from fastapi import FastAPI
import time
import random
import redis
import json
import logging
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO)

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=True,
    socket_connect_timeout=2,
    socket_timeout=2
)

@app.post("/process/{order_id}")
def process_payment(order_id: str):
    logging.info(f"[PAYMENT_SERVICE] Processing: {order_id}")

    time.sleep(2)

    try:
        data = r.get(order_id)
    except Exception as e:
        logging.error(f"[PAYMENT_SERVICE] Redis error: {e}")
        return {"error": "Redis unavailable"}

    if not data:
        return {"error": "Order not found"}

    order = json.loads(data)

    status = "CONFIRMED" if random.choice([True, False]) else "FAILED"

    order["status"] = status

    try:
        r.set(order_id, json.dumps(order))
    except Exception as e:
        logging.error(f"[PAYMENT_SERVICE] Redis error: {e}")
        return {"error": "Redis unavailable"}

    logging.info(f"[PAYMENT_SERVICE] {order_id} → {status}")

    return {"order_id": order_id, "status": status}