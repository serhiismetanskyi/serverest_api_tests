import json

from config import BASE_URI
from services.serverest_api.serverest_client import ServeRestClient


class Login(ServeRestClient):
    def __init__(self):
        super().__init__()
        self.login_url = f"{BASE_URI}/login"

    def login(self, payload):
        url = f"{self.login_url}"
        return self.request.post_request(url, json.dumps(payload), self.headers)
