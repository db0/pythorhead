from typing import Optional


class Authentication:
    token: Optional[str] = None
    api_base_url: Optional[str] = None

    def set_token(self, token: str) -> None:
        self.token = token

    def set_api_base_url(self, api_base_url: str) -> None:
        self.api_base_url = api_base_url
