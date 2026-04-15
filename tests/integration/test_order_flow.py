from framework.client.base_client import BaseClient

client = BaseClient("http://127.0.0.1:8000")

def test_order_flow():
    response = client.post("/orders", {
        "user_id": "999",
        "item": "biryani"
    })

    order_id = response.json()["order_id"]

    order = client.get(f"/orders/{order_id}")

    assert order.status_code == 200
    assert order.json()["user_id"] == "999"