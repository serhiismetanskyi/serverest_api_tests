import json

from config import BASE_URI
from services.serverest_api.serverest_client import ServeRestClient


class Products(ServeRestClient):
    def __init__(self):
        super().__init__()
        self.products_url = f"{BASE_URI}/produtos"

    def create_product(self, payload, token):
        url = f"{self.products_url}"
        self.headers_with_token["Authorization"] = token
        return self.request.post_request(url, json.dumps(payload), self.headers_with_token)

    def get_product(self, **kwargs):
        url_params = {key: value for key, value in kwargs.items() if value is not None}
        url = f"{self.products_url}?"
        url += "&".join([f"{key}={value}" for key, value in url_params.items()])
        return self.request.get_request(url, self.headers)

    def get_product_by_id(self, product_id):
        url = f"{self.products_url}/{product_id}"
        return self.request.get_request(url, self.headers)

    def update_product(self, product_id, payload, token):
        url = f"{self.products_url}/{product_id}"
        self.headers_with_token["Authorization"] = token
        return self.request.put_request(url, json.dumps(payload), self.headers_with_token)

    def delete_product(self, product_id, token):
        url = f"{self.products_url}/{product_id}"
        self.headers_with_token["Authorization"] = token
        return self.request.delete_request(url, self.headers_with_token)