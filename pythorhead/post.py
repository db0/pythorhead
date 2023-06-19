from typing import Any, Literal, Optional, List

from pythorhead.types import FeatureType, ListingType, SortType
from pythorhead.requestor import Requestor, Request


class Post:
    def __init__(self):
        self._requestor = Requestor()

    def get(
        self,
        post_id: int,
        comment_id: Optional[int] = None,
    ) -> Optional[dict]:
        """
        Get a post.

        Args:
            post_id (int)
            comment_id (int, optional) Defaults to None.

        Returns:
            dict: post view
        """
        get_post = {
            "id": post_id,
        }

        if comment_id is not None:
            get_post["comment_id"] = comment_id

        return self._requestor.request(Request.GET, "/post", params=get_post)

    def list(  # noqa: A003
        self,
        community_id: Optional[int] = None,
        community_name: Optional[str] = None,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        saved_only: Optional[bool] = None,
        sort: Optional[SortType] = None,
        type_: Optional[ListingType] = None,
    ) -> List[dict]:
        """

        Get posts, with various filters.

        Args:
            community_id (int, optional): Defaults to None.
            community_name (str, optional): Defaults to None.
            limit (int, optional): Defaults to None.
            page (int, optional): Defaults to None.
            saved_only (bool, optional): Defaults to None.
            sort (SortType, optional): Defaults to None.
            type_ (ListingType, optional): Defaults to None.

        Returns:
            list[dict]: list of posts
        """
        list_post: dict = {}

        if community_id is not None:
            list_post["community_id"] = community_id
        if community_name is not None:
            list_post["community_name"] = community_name
        if limit is not None:
            list_post["limit"] = limit
        if page is not None:
            list_post["page"] = page
        if saved_only is not None:
            list_post["saved_only"] = saved_only
        if sort is not None:
            list_post["sort"] = sort.value
        if type_ is not None:
            list_post["type_"] = type_.value
        if data := self._requestor.request(Request.GET, "/post/list", params=list_post):
            return data["posts"]
        return []

    def create(
        self,
        community_id: int,
        name: str,
        url: Optional[str] = None,
        body: Optional[str] = None,
        nsfw: Optional[bool] = None,
        honeypot: Optional[str] = None,
        language_id: Optional[int] = None,
    ) -> Optional[dict]:
        """
        Create a post

        Args:
            community_id (int)
            name (str)
            url (str, optional): Defaults to None.
            body (str, optional): Defaults to None.
            nsfw (bool, optional): Defaults to None.
            honeypot (str, optional): Defaults to None.
            language_id (int, optional): Defaults to None.

        Returns:
            Optional[dict]: post data if successful
        """
        new_post = {
            "community_id": community_id,
            "name": name,
        }

        if url is not None:
            new_post["url"] = url
        if body is not None:
            new_post["body"] = body
        if nsfw is not None:
            new_post["nsfw"] = nsfw
        if honeypot is not None:
            new_post["honeypot"] = honeypot
        if language_id is not None:
            new_post["language_id"] = language_id

        return self._requestor.request(Request.POST, "/post", json=new_post)

    def delete(self, post_id: int, deleted: bool) -> Optional[dict]:
        """
        Deletes / Restore a post

        Args:
            post_id (int)
            deleted (bool)

        Returns:
            Optional[dict]: post data if successful
        """
        delete_post = {
            "post_id": post_id,
            "deleted": deleted,
        }
        return self._requestor.request(Request.POST, "/post/delete", json=delete_post)

    def remove(self, post_id: int, removed: bool, reason: Optional[str] = None) -> Optional[dict]:
        """

        Moderator remove / restore a post.

        Args:
            post_id (int)
            removed (bool)
            reason (str, optional): Defaults to None.

        Returns:
            Optional[dict]: post data if successful
        """
        remove_post = {
            "post_id": post_id,
            "removed": removed,
        }
        if reason is not None:
            remove_post["reason"] = reason

        return self._requestor.request(Request.POST, "/post/remove", json=remove_post)

    def edit(
        self,
        post_id: int,
        name: Optional[str] = None,
        url: Optional[str] = None,
        body: Optional[str] = None,
        nsfw: Optional[bool] = None,
        language_id: Optional[int] = None,
    ) -> Optional[dict]:
        """

        Edit a post

        Args:
            post_id (int)
            name (str, optional): Defaults to None.
            url (str, optional): Defaults to None.
            body (str, optional): Defaults to None.
            nsfw (bool, optional): Defaults to None.
            language_id (int, optional): Defaults to None.

        Returns:
            Optional[dict]: post data if successful
        """
        edit_post: dict[str, Any] = {
            "post_id": post_id,
        }
        if name is not None:
            edit_post["name"] = name
        if url is not None:
            edit_post["url"] = url
        if body is not None:
            edit_post["body"] = body
        if nsfw is not None:
            edit_post["nsfw"] = nsfw
        if language_id is not None:
            edit_post["language_id"] = language_id

        return self._requestor.request(Request.PUT, "/post", json=edit_post)

    def like(self, post_id: int, score: Literal[-1, 0, 1]) -> Optional[dict]:
        """
        Like a post

        Args:
            post_id (int)
            score (int)

        Returns:
            Optional[dict]: post data if successful
        """
        like_post = {
            "post_id": post_id,
            "score": score,
        }
        return self._requestor.request(Request.POST, "/post/like", json=like_post)

    def save(self, post_id: int, saved: bool) -> Optional[dict]:
        """

        Save / Unsave a post

        Args:
            post_id (int)
            saved (bool)

        Returns:
            Optional[dict]: post data if successful
        """
        save_post = {
            "post_id": post_id,
            "save": saved,
        }
        return self._requestor.request(Request.PUT, "/post/save", json=save_post)

    def report(self, post_id: int, reason: str) -> Optional[dict]:
        """

        Report a post

        Args:
            post_id (int)
            reason (str)

        Returns:
            Optional[dict]: post report data if successful
        """
        report_post = {
            "post_id": post_id,
            "reason": reason,
        }
        return self._requestor.request(Request.POST, "/post/report", json=report_post)

    def feature(self, post_id: int, feature: bool, feature_type: FeatureType) -> Optional[dict]:
        """

        Add / Remove Feature from a post

        Args:
            post_id (int)
            feature (bool)
            feature_type (FeatureType)

        Returns:
            Optional[dict]: post data if successful
        """

        feature_post = {
            "post_id": post_id,
            "featured": feature,
            "feature_type": feature_type.value,
        }
        return self._requestor.request(Request.POST, "/post/feature", json=feature_post)

    __call__ = create
