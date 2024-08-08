import logging
from enum import Enum
from typing import Optional

import requests
import semver

from pythorhead import get_version
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
    _nodeinfo: Optional[dict] = None
    domain: Optional[str] = None
    raise_exceptions: Optional[bool] = False
    request_timeout: Optional[int] = 3
    logged_in_username: Optional[str] = None
    current_password: Optional[str] = None

    def __init__(self, raise_exceptions = False, request_timeout = 3):
        self._auth = Authentication()
        self.set_api_base_url = self._auth.set_api_base_url
        self.raise_exceptions = raise_exceptions
        self.request_timeout = request_timeout

    @property
    def nodeinfo(self) -> dict:
        if self._nodeinfo:
            return self._nodeinfo
        try:
            headers = {
                "Sec-Fetch-Dest": "document",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-User": "?1",
                "Sec-GPC": "1",
                "User-Agent": f"pythorhead/{get_version()}",
            }
            self._nodeinfo = requests.get(f"{self.domain}/nodeinfo/2.0.json", headers=headers, timeout=2).json()
            return self._nodeinfo
        except Exception as err:
            if not self.raise_exceptions:
                logger.error(f"Problem encountered retrieving Lemmy nodeinfo: {err}")
                return {}
            raise err

    def get_instance_version(self):
        return semver.Version.parse(self.nodeinfo["software"]["version"])

    def set_domain(self, domain: str):
        self.domain = domain
        self._auth.set_api_base_url(self.domain)
        software = self.nodeinfo.get("software", {}).get("name")
        if software != "lemmy":
            logger.error(f"Domain name does not appear to contain a lemmy software, but instead '{software}")
            return
        logger.info(f"Connected succesfully to Lemmy v{self.nodeinfo['software']['version']} instance {self.domain}")

    def api(self, method: Request, endpoint: str, **kwargs) -> Optional[dict]:
        logger.info(f"Requesting API {method} {endpoint}")
        headers = {
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Sec-GPC": "1",
            "User-Agent": f"pythorhead/{get_version()}",
        }
        if self._auth.token:
            # < 0.19 requires a different auth method
            if self.get_instance_version().compare("0.19.0") < 0:
                if (data := kwargs.get("json")) is not None:
                    data["auth"] = self._auth.token
                if (data := kwargs.get("params")) is not None:
                    data["auth"] = self._auth.token
            else:
                headers["Authorization"] = f"Bearer {self._auth.token}"
        try:
            r = REQUEST_MAP[method](f"{self._auth.api_url}{endpoint}", headers = headers, timeout=self.request_timeout , **kwargs)
        except Exception as err:
            if not self.raise_exceptions:
                logger.error(f"Error encountered while {method} on endpoint {endpoint}: {err}")
                return
            raise err
        if not r.ok:
            if not self.raise_exceptions:
                logger.error(f"Error encountered while {method} on endpoint {endpoint}: {r.text}")
                return
            else:
                raise Exception(f"Error encountered while {method} on endpoint {endpoint}: {r.text}")

        return r.json()

    def image(self, method: Request, **kwargs) -> Optional[dict]:
        logger.info(f"Requesting image {method}")
        cookies = {}
        if self._auth.token:
            cookies["jwt"] = self._auth.token
        r = REQUEST_MAP[method](self._auth.image_url, cookies=cookies, timeout=self.request_timeout, **kwargs)
        if not r.ok:
            if not self.raise_exceptions:
                logger.error(f"Error encountered while {method}: {r.text}")
                return
            else:
                raise Exception(f"Error encountered while {method}: {r.text}")
        return r.json()

    def image_del(self, method: Request, image_delete_url:str, **kwargs) -> Optional[dict]:
        logger.info(f"Deleting image {method}")
        cookies = {}
        if self._auth.token:
            cookies["jwt"] = self._auth.token
        r = REQUEST_MAP[method](image_delete_url, cookies=cookies, timeout=self.request_timeout, **kwargs)
        if not r.ok:
            if not self.raise_exceptions:
                logger.error(f"Error encountered while {method}: {r.text}")
                return
            else:
                raise Exception(f"Error encountered while {method}: {r.text}")
        return r

    def log_in(self, username_or_email: str, password: str, totp: Optional[str] = None) -> bool:
        self.logged_in_username = username_or_email
        self.current_password = password
        return self._log_in(totp)

    def _log_in(self, totp: Optional[str] = None) -> bool:
        payload = {
            "username_or_email": self.logged_in_username,
            "password": self.current_password,
            "totp_2fa_token": totp,
        }
        if data := self.api(Request.POST, "/user/login", json=payload):
            self._auth.set_token(data["jwt"])
        else:
            self.logged_in_username = None
            self.current_password = None
        return self._auth.token is not None

    def log_out(self) -> None:
        self._auth.token = None
        self.logged_in_username = None

    def is_logged_in(self) -> bool:
        return self.logged_in_username is not None
