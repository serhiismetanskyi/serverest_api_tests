from services.base_client import BaseClient
from utils.request import APIRequest


class ServeRestClient(BaseClient):
    def __init__(self):
        super().__init__()
        self.request = APIRequest()

    # TODO: Add test after implemented
    def get_service_status(self):
        pass
