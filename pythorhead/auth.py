from typing import Optional


# Stack Overflow: Creating a singleton in Python
# https://stackoverflow.com/q/6760685
# CC BY-SA 3.0
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Authentication(metaclass=Singleton):
    token: Optional[str] = None
    api_base_url: Optional[str] = None

    def set_token(self, token: str) -> None:
        self.token = token

    def set_api_base_url(self, api_base_url: str) -> None:
        self.api_base_url = api_base_url
