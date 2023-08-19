import os
import requests

from core.custom_error import bad_request, not_found


class BaseService:
    def __init__(self) -> None:
        self.url = os.getenv('BASE_BIN_DOMAIN')

    def get(self, url: str, headers: dict = None) -> requests.models.Response:
        endpoint = self.url + url

        try:
            return requests.get(endpoint,
                                headers=self.generate_common_header_request(
                                    headers),
                                verify=False)
        except:
            return bad_request(http_method='POST')

    def post(self, url: str, data: dict = None, json: dict = None, headers: dict = None) -> requests.models.Response:
        endpoint = self.url + url

        try:
            return requests.post(endpoint,
                                 headers=self.generate_common_header_request(
                                     headers),
                                 data=data,
                                 json=json,
                                 verify=False)
        except:
            return bad_request(http_method='POST')

    def postImage(self, url: str, files, headers: dict = None) -> requests.models.Response:
        endpoint = self.url + url

        try:
            with requests.Session() as s:
                res = requests.post(endpoint,
                                    files=files,
                                    headers=self.generate_common_header_request(
                                        headers),
                                    verify=False,
                                    )
                return res
        except:
            return bad_request(http_method='POST')

    def generate_common_header_request(self, headers: dict = None) -> dict:
        default_header = {
            'X-Bin-ID': os.getenv('X_BIN_ID'),
            'X-Bin-Client': os.getenv('X_BIN_CLIENT'),
            'Content-Type': 'application/json'
        }

        if headers:
            for k in headers:
                default_header[k] = headers[k]

        return default_header
