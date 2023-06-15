import requests
from loguru import logger

from pythorhead.post import post


class Lemmy:
    _auth_token = None
    _api_base_url = None
    _known_communities = {}
    post = None

    def __init__(self, api_base_url) -> None:
        self._api_base_url = api_base_url

    def log_in(self, username_or_email: str, password: str) -> bool:
        payload = {
            "username_or_email": username_or_email,
            "password": password,
        }
        try:
            re = requests.post(f"{self._api_base_url}/api/v3/user/login", json=payload)
            self._auth_token = re.json()["jwt"]
            self.post = post(self._api_base_url, self._auth_token)

        except Exception as err:
            logger.error(f"Something went wrong while logging in as {username_or_email}: {err}")
            return False
        return True

    def discover_community(self, community_name: str) -> int | None:
        if community_name in self._known_communities:
            return self._known_communities[community_name]
        try:
            req = requests.get(f"{self._api_base_url}/api/v3/community?name={community_name}")
            community_id = req.json()["community_view"]["community"]["id"]
            self._known_communities[community_name] = community_id
        except Exception as err:
            logger.error(f"Error when looking up community '{community_name}': {err}")
            return
        return community_id
