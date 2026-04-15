import time
from framework.client.base_client import BaseClient

client = BaseClient("http://127.0.0.1:8000")

def test_async_queue_processing():
    response = client.post("/orders", {
        "user_id": "123",
        "item": "pizza"
    })

    order_id = response.json()["order_id"]

    # Initial state check
    order = client.get(f"/orders/{order_id}")
    assert order.json()["status"] == "CREATED"

    # Polling instead of fixed sleep
    timeout = 5  # max wait time
    interval = 0.5  # retry interval
    start_time = time.time()

    final_status = None

    while time.time() - start_time < timeout:
        order = client.get(f"/orders/{order_id}")
        final_status = order.json()["status"]

        if final_status in ["CONFIRMED", "FAILED"]:
            break

        time.sleep(interval)

    # Step 3: Final assertion
    assert final_status in ["CONFIRMED", "FAILED"]