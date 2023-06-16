import requests
from loguru import logger

from pythorhead.auth import Authentication
from pythorhead.post import Post


class Lemmy:
    post: Post
    _auth: Authentication
    _known_communities = {}

    def __init__(self, api_base_url: str) -> None:
        self._auth = Authentication()
        self._auth.api_base_url = f"{api_base_url}/api/v3"
        self.post = Post()

    def log_in(self, username_or_email: str, password: str) -> bool:
        return Authentication().log_in(username_or_email, password)

    def discover_community(self, community_name: str) -> int | None:
        if community_name in self._known_communities:
            return self._known_communities[community_name]
        try:
            req = requests.get(f"{self._auth.api_base_url}/community?name={community_name}")
            community_id = req.json()["community_view"]["community"]["id"]
            self._known_communities[community_name] = community_id
        except Exception as err:
            logger.error(f"Error when looking up community '{community_name}': {err}")
            return
        return community_id
