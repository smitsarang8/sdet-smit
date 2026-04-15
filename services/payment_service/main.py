from fastapi import FastAPI
import time
import random
import redis
import json

app = FastAPI()

r = redis.Redis(host="redis", port=6379, decode_responses=True)


@app.post("/process/{order_id}")
def process_payment(order_id: str):
    time.sleep(2)

    data = r.get(order_id)

    if not data:
        return {"error": "Order not found"}

    order = json.loads(data)

    status = "CONFIRMED" if random.choice([True, False]) else "FAILED"

    order["status"] = status

    r.set(order_id, json.dumps(order))

    print(f"[Payment Service] {order_id} → {status}")

    return {"order_id": order_id, "status": status}