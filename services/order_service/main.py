from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import threading
from queue import Queue
import requests
import redis
import json
import logging
import time
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
PAYMENT_URL = os.getenv("PAYMENT_URL", "http://localhost:8001")
MAX_RETRIES = 3

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2
)

class OrderRequest(BaseModel):
    user_id: str
    item: str

order_queue = Queue()

def order_worker():
    while True:
        order_id = order_queue.get()
        logging.info(f"[ORDER_SERVICE] Processing: {order_id}")

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = requests.post(
                    f"{PAYMENT_URL}/process/{order_id}",
                    timeout=5
                )

                if response.status_code == 200:
                    logging.info(f"[ORDER_SERVICE] {order_id} → SUCCESS")
                    break

            except Exception as e:
                logging.error(f"[ORDER_SERVICE] {order_id} → ERROR: {str(e)}")

            time.sleep(1)

        else:
            logging.error(f"[ORDER_SERVICE] {order_id} → FINAL FAILURE")

            try:
                data = r.get(order_id)
                if data:
                    order = json.loads(data)
                    order["status"] = "FAILED"
                    r.set(order_id, json.dumps(order))
            except Exception as e:
                logging.error(f"[ORDER_SERVICE] Redis failure: {e}")

        order_queue.task_done()

@app.on_event("startup")
def start_worker():
    threading.Thread(target=order_worker, daemon=True).start()
    logging.info("[ORDER_SERVICE] Worker started")

@app.post("/orders")
def create_order(order: OrderRequest):
    order_id = str(uuid.uuid4())

    data = {
        "user_id": order.user_id,
        "item": order.item,
        "status": "CREATED"
    }

    try:
        r.set(order_id, json.dumps(data))
    except Exception as e:
        logging.error(f"[ORDER_SERVICE] Redis error: {e}")
        return {"error": "Redis unavailable"}

    order_queue.put(order_id)

    logging.info(f"[ORDER_SERVICE] Order queued: {order_id}")

    return {"order_id": order_id, "status": "CREATED"}

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    try:
        data = r.get(order_id)
    except Exception as e:
        logging.error(f"[ORDER_SERVICE] Redis error: {e}")
        return {"error": "Redis unavailable"}

    if not data:
        return {"error": "Order not found"}

    return json.loads(data)