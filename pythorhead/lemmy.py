import logging
import time
from typing import Any, Optional

from pythorhead.comment import Comment
from pythorhead.community import Community
from pythorhead.image import Image
from pythorhead.mention import Mention
from pythorhead.post import Post
from pythorhead.private_message import PrivateMessage
from pythorhead.requestor import Request, Requestor
from pythorhead.site import Site
from pythorhead.types import FeatureType, ListingType, SortType, SearchType, SearchOption
from pythorhead.user import User
from pythorhead.admin import Admin

logger = logging.getLogger(__name__)

class Lemmy:
    _known_communities = {}
    _requestor: Requestor

    def __init__(self, api_base_url: str) -> None:
        self._requestor = Requestor()
        self._requestor.set_domain(api_base_url)
        self.post = Post(self._requestor)
        self.community = Community(self._requestor)
        self.comment = Comment(self._requestor)
        self.site = Site(self._requestor)
        self.user = User(self._requestor)
        self.private_message = PrivateMessage(self._requestor)
        self.image = Image(self._requestor)
        self.mention = Mention(self._requestor)
        self.admin = Admin(self._requestor)

    @property
    def nodeinfo(self):
        return self._requestor.nodeinfo

    def log_in(self, username_or_email: str, password: str, totp: Optional[str] = None) -> bool:
        return self._requestor.log_in(username_or_email, password, totp)

    def discover_community(self, community_name: str, search=SearchOption.Yes) -> Optional[int]:
        if community_name in self._known_communities:
            return self._known_communities[community_name]

        request = self.community.get(name=community_name)
        logger.warning(request)
        logger.warning(search)
        if request is None and search != SearchOption.No:
            search_result = self.search(
                q=community_name,
                type_=SearchType.Communities.value
            )
            logger.warning(search_result)
            if search_result is None:
                logger.warning(search != SearchOption.Retry)
                if search != SearchOption.Retry:
                    return None
                logger.warning(f"Community '{community_name}' not found via search. Attempting wait and retry")
                time.sleep(5)
                search_result = self.search(
                    q=community_name,
                    type_=SearchType.Communities.value
                )
                logger.warning(search_result)
                if search_result is not None:
                    request = self.community.get(name=community_name)
        if request is not None:
            community_id = request["community_view"]["community"]["id"]
            self._known_communities[community_name] = community_id
            return community_id

    def search(
        self,
        q: str,
        community_id: Optional[int] = None,
        community_name: Optional[str] = None,
        creator_id: Optional[int] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        listing_type: Optional[ListingType] = None,
        sort: Optional[SortType] = None,
        type_: Optional[SearchType] = None,
    ) -> Optional[dict]:
        """

        Search on lemmy

        Args:
            q (str)
            community_id (Optional[int]): Defaults to None.
            community_name (Optional[str]): Defaults to None.
            creator_id (Optional[int]): Defaults to None.
            page (Optional[int]): Defaults to None.
            limit (Optional[int]): Defaults to None.
            listing_type (Optional[ListingType]): Defaults to None.
            sort (Optional[SortType]): Defaults to None.
            type_ (Optional[SearchType]): Defaults to None.

        Returns:
            Optional[dict]: search result
        """

        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != "self"}
        return self._requestor.api(Request.GET, "/search", params=params)
