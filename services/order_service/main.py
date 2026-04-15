from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import threading
import time
import random
from queue import Queue

app = FastAPI()

class OrderRequest(BaseModel):
    user_id: str
    item: str

orders = {}
order_queue = Queue()

def order_worker():
    while True:
        order_id = order_queue.get()

        time.sleep(2)

        status = "CONFIRMED" if random.choice([True, False]) else "FAILED"
        orders[order_id]["status"] = status

        order_queue.task_done()

@app.on_event("startup")
def start_worker():
    thread = threading.Thread(target=order_worker, daemon=True)
    thread.start()


@app.post("/orders")
def create_order(order: OrderRequest):
    order_id = str(uuid.uuid4())

    orders[order_id] = {
        "user_id": order.user_id,
        "item": order.item,
        "status": "CREATED"
    }

    order_queue.put(order_id)

    return {
        "order_id": order_id,
        "status": "CREATED"
    }


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    return orders.get(order_id, {"error": "Order not found"})