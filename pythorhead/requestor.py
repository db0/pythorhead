import requests
import logging

from enum import Enum
from typing import Optional
from pythorhead.auth import Authentication


logger = logging.getLogger(__name__)


class Request(Enum):
    GET = "GET"
    PUT = "PUT"
    POST = "POST"


REQUEST_MAP = {
    Request.GET: requests.get,
    Request.PUT: requests.put,
    Request.POST: requests.post,
}


class Requestor:
    def __init__(self):
        self._auth = Authentication()
        self.set_api_base_url = self._auth.set_api_base_url

    def request(self, method: Request, endpoint: str, **kwargs) -> Optional[dict]:
        logger.info(f"Requesting {method} {endpoint}")
        if self._auth.token:
            if (data := kwargs.get("json")) is not None:
                data["auth"] = self._auth.token
            if (data := kwargs.get("params")) is not None:
                data["auth"] = self._auth.token

        r = REQUEST_MAP[method](f"{self._auth.api_base_url}{endpoint}", **kwargs)

        if not r.ok:
            logger.error(f"Error encountered while {method}: {r.text}")
            return

        return r.json()

    def log_in(self, username_or_email: str, password: str) -> bool:
        payload = {
            "username_or_email": username_or_email,
            "password": password,
        }
        if data := self.request(Request.POST, "/user/login", json=payload):
            self._auth.set_token(data["jwt"])
        return self._auth.token is not None

    def log_out(self) -> None:
        self._auth.token = None
