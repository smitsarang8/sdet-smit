import requests

class BaseClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, path, data):
        return requests.post(
            f"{self.base_url}{path}",
            json=data,
            timeout=5
        )

    def get(self, path):
        return requests.get(
            f"{self.base_url}{path}",
            timeout=5
        )