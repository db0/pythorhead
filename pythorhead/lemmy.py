from __future__ import annotations
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
from pythorhead.emoji import Emoji
from pythorhead.classes.user import LemmyUser
from pythorhead import class_methods

logger = logging.getLogger(__name__)

class Lemmy:
    _known_communities = {}
    _requestor: Requestor
    post: Post
    community: Community
    comment: Comment
    site: Site
    user: User
    private_message: PrivateMessage
    image: Image
    mention: Mention
    admin: Admin
    emoji: Emoji
    # imported class methods
    get_user = class_methods.get_user
    get_registration_applications = class_methods.get_applications

    def __init__(self, api_base_url: str, raise_exceptions = False, request_timeout=3) -> None:
        self._requestor = Requestor(raise_exceptions, request_timeout)
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
        self.emoji = Emoji(self._requestor)

    @property
    def nodeinfo(self):
        return self._requestor.nodeinfo

    @property
    def username(self):
        return self._requestor.logged_in_username

    @property
    def instance_version(self):
        return self._requestor.get_instance_version()
    
    def log_in(self, username_or_email: str, password: str, totp: Optional[str] = None) -> bool:
        return self._requestor.log_in(username_or_email, password, totp)

    def relog_in(self) -> bool:
        return self._requestor._log_in()

    def discover_community(self, community_name: str, search=SearchOption.Retry) -> Optional[int]:
        if community_name in self._known_communities:
            return self._known_communities[community_name]

        request = self.community.get(name=community_name)
        if request is None and search != SearchOption.No:
            search_result = self.search(
                q=community_name,
                type_=SearchType.Communities
            )
            if search_result is None:
                return None
            if len(search_result['communities']) == 0:
                if search != SearchOption.Retry:
                    return None
                logger.info(f"Community '{community_name}' not found via search. Attempting wait and retry")
                time.sleep(5)
                search_result = self.search(
                    q=community_name,
                    type_=SearchType.Communities
                )
                if len(search_result['communities']) > 0:
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
        if listing_type is not None:
            listing_type = listing_type.value
        if sort is not None:
            sort = sort.value
        if type_ is not None:
            type_ = type_.value
        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != "self"}
        return self._requestor.api(Request.GET, "/search", params=params)

    def resolve_object(
        self,
        q: str,
    ) -> Optional[dict]:
        """

        Resolve a remove URL to the local URL

        Args:
            q (str)

        Returns:
            Optional[dict]: search result
        """
        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != "self"}
        return self._requestor.api(Request.GET, "/resolve_object", params=params)

    def get_base_url(self):
        return self._requestor.domain
    
