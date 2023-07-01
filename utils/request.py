from dataclasses import dataclass

import requests

from utils.logger import Logger


@dataclass
class APIResponse:
    status_code: int
    text: str
    as_dict: object
    headers: dict


class APIRequest:
    def get_request(self, url, headers):
        Logger.add_request(url, method="GET")
        response = requests.get(url=url, headers=headers)
        Logger.add_response(response)
        return self.get_responses(response)

    def post_request(self, url, payload, headers):
        Logger.add_request(url, method="POST")
        response = requests.post(url=url, data=payload, headers=headers)
        Logger.add_response(response)
        return self.get_responses(response)

    def put_request(self, url, payload, headers):
        Logger.add_request(url, method="PUT")
        response = requests.put(url=url, data=payload, headers=headers)
        Logger.add_response(response)
        return self.get_responses(response)

    def delete_request(self, url, headers):
        Logger.add_request(url, method="DELETE")
        response = requests.delete(url=url, data=None, headers=headers)
        Logger.add_response(response)
        return self.get_responses(response)

    @staticmethod
    def get_responses(response):
        status_code = response.status_code
        text = response.text
        try:
            as_dict = response.json()
        except ValueError:
            as_dict = {}
        headers = response.headers
        return APIResponse(status_code, text, as_dict, headers)