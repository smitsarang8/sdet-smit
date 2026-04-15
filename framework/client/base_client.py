import requests

class BaseClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def post(self, endpoint, data=None):
        return requests.post(f"{self.base_url}{endpoint}", json=data)

    def get(self, endpoint):
        return requests.get(f"{self.base_url}{endpoint}")