import requests
from loguru import logger


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Authentication(metaclass=Singleton):
    token = None
    api_base_url = None

    def log_in(self, username_or_email: str, password: str) -> bool:
        payload = {
            "username_or_email": username_or_email,
            "password": password,
        }
        try:
            re = requests.post(f"{self.api_base_url}/api/v3/user/login", json=payload)
            self.token = re.json()["jwt"]

        except Exception as err:
            logger.error(f"Something went wrong while logging in as {username_or_email}: {err}")
            return False
        return True

    def _set_base_url(self, api_base_url: str):
        self.api_base_url = api_base_url

    def log_out(self):
        self.token = None
