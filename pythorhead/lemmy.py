import logging
from typing import Optional

from pythorhead.comment import Comment
from pythorhead.post import Post
from pythorhead.site import Site
from pythorhead.requestor import Request, Requestor

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class Lemmy:
    post: Post
    comment: Comment
    _known_communities = {}
    _requestor: Requestor

    def __init__(self, api_base_url: str) -> None:
        self._requestor = Requestor()
        self._requestor.set_api_base_url(f"{api_base_url}/api/v3")
        self.post = Post()
        self.comment = Comment()
        self.site = Site()

    def log_in(self, username_or_email: str, password: str) -> bool:
        return self._requestor.log_in(username_or_email, password)

    def discover_community(self, community_name: str) -> Optional[int]:
        if community_name in self._known_communities:
            return self._known_communities[community_name]

        request = self._requestor.request(Request.GET, "/community", params={"name": community_name})

        if request is not None:
            community_id = request["community_view"]["community"]["id"]
            self._known_communities[community_name] = community_id
            return community_id
