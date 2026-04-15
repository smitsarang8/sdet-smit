from locust import HttpUser, task

class OrderUser(HttpUser):
    host = "http://127.0.0.1:8000"

    @task
    def place_order(self):
        self.client.post("/orders", json={
            "user_id": "load_test",
            "item": "pizza"
        })