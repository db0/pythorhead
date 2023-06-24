import logging
from typing import Optional

from pythorhead.comment import Comment
from pythorhead.image import Image
from pythorhead.post import Post
from pythorhead.private_message import PrivateMessage
from pythorhead.requestor import Request, Requestor
from pythorhead.site import Site
from pythorhead.user import User

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class Lemmy:
    _known_communities = {}
    _requestor: Requestor

    def __init__(self, api_base_url: str) -> None:
        self._requestor = Requestor()
        self._requestor.set_domain(api_base_url)
        self.post = Post(self._requestor)
        self.comment = Comment(self._requestor)
        self.site = Site(self._requestor)
        self.user = User(self._requestor)
        self.private_message = PrivateMessage(self._requestor)
        self.image = Image(self._requestor)

    @property
    def nodeinfo(self):
        return self._requestor.nodeinfo

    def log_in(self, username_or_email: str, password: str) -> bool:
        return self._requestor.log_in(username_or_email, password)

    def discover_community(self, community_name: str) -> Optional[int]:
        if community_name in self._known_communities:
            return self._known_communities[community_name]

        request = self._requestor.api(Request.GET, "/community", params={"name": community_name})

        if request is not None:
            community_id = request["community_view"]["community"]["id"]
            self._known_communities[community_name] = community_id
            return community_id
