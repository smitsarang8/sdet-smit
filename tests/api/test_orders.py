from framework.client.base_client import BaseClient

client = BaseClient("http://127.0.0.1:8000")

def test_create_order():
    response = client.post("/orders", {
        "user_id": "123",
        "item": "pizza"
    })

    assert response.status_code == 200
    assert "order_id" in response.json()