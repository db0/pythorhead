from typing import Optional


class Authentication:
    token: Optional[str] = None
    api_url: Optional[str] = None

    def set_token(self, token: str) -> None:
        self.token = token

    def set_api_base_url(self, base_url: str) -> None:
        self.api_url = f"{base_url}/api/v3"
        self.image_url = f"{base_url}/pictrs/image"
