from typing import Any, Literal

import requests
from loguru import logger

from pythorhead.auth import Authentication
from pythorhead.types.listing import ListingType
from pythorhead.types.sort import SortType


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

        re = requests.get(f"{self._auth.api_base_url}/api/v3/post", params=get_post)
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
            list_post["sort"] = sort
        if type_ is not None:
            list_post["type_"] = type_

        re = requests.get(f"{self._auth.api_base_url}/api/v3/post/list", params=list_post)
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

        re = requests.post(f"{self._auth.api_base_url}/api/v3/post", json=new_post)

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
        re = requests.post(f"{self._auth.api_base_url}/api/v3/post/delete", json=delete_post)
        if not re.ok:
            logger.error(f"Error encountered while deleting post: {re.text}")
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
        re = requests.put(f"{self._auth.api_base_url}/api/v3/post", json=edit_post)
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
        re = requests.post(f"{self._auth.api_base_url}/api/v3/post/like", json=like_post)
        if not re.ok:
            logger.error(f"Error encountered while liking post: {re.text}")
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

        re = requests.post(f"{self._auth.api_base_url}/api/v3/post/report", json=report_post)
        if not re.ok:
            logger.error(f"Error encountered while reporting post: {re.text}")
        return re.ok

    __call__ = create
