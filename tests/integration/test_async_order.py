import time
from framework.client.base_client import BaseClient

client = BaseClient("http://127.0.0.1:8000")

def test_async_queue_processing():
    response = client.post("/orders", {
        "user_id": "123",
        "item": "pizza"
    })

    order_id = response.json()["order_id"]

    # Initial state
    order = client.get(f"/orders/{order_id}")
    assert order.json()["status"] == "CREATED"

    # ✅ POLLING INSTEAD OF FIXED SLEEP
    timeout = 5
    start_time = time.time()

    while time.time() - start_time < timeout:
        order = client.get(f"/orders/{order_id}")
        status = order.json()["status"]

        if status in ["CONFIRMED", "FAILED"]:
            break

        time.sleep(0.5)

    assert status in ["CONFIRMED", "FAILED"]