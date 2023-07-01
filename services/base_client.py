class BaseClient:

    def __init__(self):
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        self.headers_with_token = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": ""
        }
