import requests
from loguru import logger


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Authentication(metaclass=Singleton):
    token: str | None = None
    api_base_url: str | None = None

    def log_in(self, username_or_email: str, password: str) -> bool:
        payload = {
            "username_or_email": username_or_email,
            "password": password,
        }
        try:
            re = requests.post(f"{self.api_base_url}/user/login", json=payload)
            self.token = re.json()["jwt"]

        except Exception as err:
            logger.error(f"Something went wrong while logging in as {username_or_email}: {err}")
            return False
        return True

    def log_out(self) -> None:
        self.token = None
