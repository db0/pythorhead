from typing import Any, Literal

import requests
from loguru import logger

from pythorhead.auth import Authentication
from pythorhead.types import FeatureType, ListingType, SortType


class Post:
    def __init__(self):
        self._auth = Authentication()

    def get(
        self,
        post_id: int,
        comment_id: int | None = None,
    ) -> dict:
        """
        Get a post.

        Args:
            post_id (int)
            comment_id (int, optional) Defaults to None.

        Returns:
            dict: post view
        """
        get_post = {
            "auth": self._auth.token,
            "id": post_id,
        }

        if comment_id is not None:
            get_post["comment_id"] = comment_id

        re = requests.get(f"{self._auth.api_base_url}/post", params=get_post)
        if not re.ok:
            logger.error(f"Error encountered while getting posts: {re.text}")
            return {}
        return re.json()

    def list(  # noqa: A003
        self,
        community_id: int | None = None,
        community_name: str | None = None,
        limit: int | None = None,
        page: int | None = None,
        saved_only: bool | None = None,
        sort: SortType | None = None,
        type_: ListingType | None = None,
    ) -> list[dict]:
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
        list_post: dict[str, Any] = {
            "auth": self._auth.token,
        }

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

        re = requests.get(f"{self._auth.api_base_url}/post/list", params=list_post)
        if not re.ok:
            logger.error(f"Error encountered while getting posts: {re.text}")
            return []
        return re.json()["posts"]

    def create(
        self,
        community_id: int,
        name: str,
        url: str | None = None,
        body: str | None = None,
        nsfw: bool | None = None,
        honeypot: str | None = None,
        language_id: int | None = None,
    ) -> bool:
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
            bool: True if successful
        """
        new_post = {
            "auth": self._auth.token,
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

        re = requests.post(f"{self._auth.api_base_url}/post", json=new_post)

        if not re.ok:
            logger.error(f"Error encountered while posting: {re.text}")

        return re.ok

    def delete(self, post_id: int, deleted: bool) -> bool:
        """
        Deletes / Restore a post

        Args:
            post_id (int)
            deleted (bool)

        Returns:
            bool: True if successful
        """
        delete_post = {
            "auth": self._auth.token,
            "post_id": post_id,
            "deleted": deleted,
        }
        re = requests.post(f"{self._auth.api_base_url}/post/delete", json=delete_post)
        if not re.ok:
            logger.error(f"Error encountered while deleting post: {re.text}")
        return re.ok

    def remove(self, post_id: int, removed: bool, reason: str | None = None) -> bool:
        """

        Moderator remove / restore a post.

        Args:
            post_id (int)
            removed (bool)
            reason (str, optional): Defaults to None.

        Returns:
            bool: True if successful
        """
        remove_post = {
            "auth": self._auth.token,
            "post_id": post_id,
            "removed": removed,
        }
        if reason is not None:
            remove_post["reason"] = reason
        re = requests.post(f"{self._auth.api_base_url}/post/remove", json=remove_post)
        if not re.ok:
            logger.error(f"Error encountered while removing post: {re.text}")
        return re.ok

    def edit(
        self,
        post_id: int,
        name: str | None = None,
        url: str | None = None,
        body: str | None = None,
        nsfw: bool | None = None,
        language_id: int | None = None,
    ) -> bool:
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
            bool: True if successful
        """
        edit_post = {
            "auth": self._auth.token,
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
        re = requests.put(f"{self._auth.api_base_url}/post", json=edit_post)
        if not re.ok:
            logger.error(f"Error encountered while editing post: {re.text}")
        return re.ok

    def like(self, post_id: int, score: Literal[-1, 0, 1]) -> bool:
        """
        Like a post

        Args:
            post_id (int)
            score (int)

        Returns:
            bool: True if successful
        """
        like_post = {
            "auth": self._auth.token,
            "post_id": post_id,
            "score": score,
        }
        re = requests.post(f"{self._auth.api_base_url}/post/like", json=like_post)
        if not re.ok:
            logger.error(f"Error encountered while liking post: {re.text}")
        return re.ok

    def save(self, post_id: int, saved: bool) -> bool:
        """

        Save / Unsave a post

        Args:
            post_id (int)
            saved (bool)

        Returns:
            bool: True if successful
        """
        save_post = {
            "auth": self._auth.token,
            "post_id": post_id,
            "save": saved,
        }
        re = requests.put(f"{self._auth.api_base_url}/post/save", json=save_post)
        if not re.ok:
            logger.error(f"Error encountered while saving post: {re.text}")
        return re.ok

    def report(self, post_id: int, reason: str) -> bool:
        """

        Report a post

        Args:
            post_id (int)
            reason (str)

        Returns:
            bool: True if successful
        """
        report_post = {
            "auth": self._auth.token,
            "post_id": post_id,
            "reason": reason,
        }

        re = requests.post(f"{self._auth.api_base_url}/post/report", json=report_post)
        if not re.ok:
            logger.error(f"Error encountered while reporting post: {re.text}")
        return re.ok

    def feature(self, post_id: int, feature: bool, feature_type: FeatureType) -> bool:
        """

        Add / Remove Feature from a post

        Args:
            post_id (int):
            feature (bool):
            feature_type (FeatureType)

        Returns:
            bool: True if successful
        """

        feature_post = {
            "auth": self._auth.token,
            "post_id": post_id,
            "featured": feature,
            "feature_type": feature_type.value,
        }
        re = requests.post(f"{self._auth.api_base_url}/post/feature", json=feature_post)
        if not re.ok:
            logger.error(f"Error encountered while feature post: {re.text}")
        return re.ok

    __call__ = create
