import json

from config import BASE_URI
from services.serverest_api.serverest_client import ServeRestClient


class Users(ServeRestClient):
    def __init__(self):
        super().__init__()
        self.users_url = f"{BASE_URI}/usuarios"

    def create_user(self, payload):
        url = f"{self.users_url}"
        return self.request.post_request(url, json.dumps(payload), self.headers)

    def get_user(self, **kwargs):
        url_params = {key: value for key, value in kwargs.items() if value is not None}
        url = f"{self.users_url}?"
        url += "&".join([f"{key}={value}" for key, value in url_params.items()])
        return self.request.get_request(url, self.headers)

    def get_user_by_id(self, user_id):
        url = f"{self.users_url}/{user_id}"
        return self.request.get_request(url, self.headers)

    def update_user(self, user_id, payload):
        url = f"{self.users_url}/{user_id}"
        return self.request.put_request(url, json.dumps(payload), self.headers)

    def delete_user(self, user_id):
        url = f"{self.users_url}/{user_id}"
        return self.request.delete_request(url, self.headers)