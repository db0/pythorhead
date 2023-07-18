from typing import Any, List, Literal, Optional, Union

from pythorhead.requestor import Request, Requestor
from pythorhead.types import FeatureType, LanguageType, ListingType, SortType


class Post:
    def __init__(self, _requestor: Requestor):
        self._requestor = _requestor

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

        return self._requestor.api(Request.GET, "/post", params=get_post)

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
        if data := self._requestor.api(Request.GET, "/post/list", params=list_post):
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
        language_id: Union[int, LanguageType, None] = None,
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
            language_id (Union[int, LanguageType], optional): Defaults to None.

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
            if isinstance(language_id, LanguageType):
                new_post["language_id"] = language_id.value
            else:
                new_post["language_id"] = language_id

        return self._requestor.api(Request.POST, "/post", json=new_post)

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
        return self._requestor.api(Request.POST, "/post/delete", json=delete_post)

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

        return self._requestor.api(Request.POST, "/post/remove", json=remove_post)

    def edit(
        self,
        post_id: int,
        name: Optional[str] = None,
        url: Optional[str] = None,
        body: Optional[str] = None,
        nsfw: Optional[bool] = None,
        language_id: Union[int, LanguageType, None] = None,
    ) -> Optional[dict]:
        """

        Edit a post

        Args:
            post_id (int)
            name (str, optional): Defaults to None.
            url (str, optional): Defaults to None.
            body (str, optional): Defaults to None.
            nsfw (bool, optional): Defaults to None.
            language_id (Union[int, LanguageType], optional): Defaults to None.

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
            if isinstance(language_id, LanguageType):
                edit_post["language_id"] = language_id.value
            else:
                edit_post["language_id"] = language_id

        return self._requestor.api(Request.PUT, "/post", json=edit_post)

    def like(self, post_id: int, score: Literal[-1, 0, 1]) -> Optional[dict]:
        """
        Like / Dislike a post

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
        return self._requestor.api(Request.POST, "/post/like", json=like_post)

    def save(self, post_id: int, saved: bool) -> Optional[dict]:
        """

        Add / Remove a post to saved posts

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
        return self._requestor.api(Request.PUT, "/post/save", json=save_post)

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
        return self._requestor.api(Request.POST, "/post/report", json=report_post)

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
        return self._requestor.api(Request.POST, "/post/feature", json=feature_post)

    def lock(self, post_id: int, locked: bool) -> Optional[dict]:
        """

        A moderator can lock a post ( IE disable new comments )

        Args:
            post_id (int)
            locked (bool)

        Returns:
            Optional[dict]: post data if successful
        """

        lock_post = {
            "post_id": post_id,
            "locked": locked,
        }
        return self._requestor.api(Request.POST, "/post/lock", json=lock_post)

    def mark_as_read(self, post_id: int, read: bool) -> Optional[dict]:
        """

        Mark a post as read

        Args:
            post_id (int)
            read (bool)

        Returns:
            Optional[dict]: post data if successful
        """

        mark_as_read_post = {
            "post_id": post_id,
            "read": read,
        }
        return self._requestor.api(Request.POST, "/post/mark_as_read", json=mark_as_read_post)

    def site_metadata(self, url: str) -> Optional[dict]:
        """

        Fetch metadata for any given site.

        Args:
            url (str)

        Returns:
            Optional[dict]: post data if successful
        """

        site_metadata_post = {
            "url": url,
        }
        return self._requestor.api(Request.GET, "/post/site_metadata", params=site_metadata_post)

    def report_list(
            self,
            community_id: Optional[int] = None,
            limit: Optional[int] = None,
            page: Optional[int] = None,
            unresolved_only: Optional[bool] = None,
    ) -> List[dict]:
        """
        Returns a list of reported posts

        https://github.com/LemmyNet/lemmy/blob/main/crates/api/src/post_report/list.rs#L14

        Args:
            community_id: Optional[int], defaults to None
            unresolved_only: Optional[bool], defaults to None
            limit: Optional[int], defaults to None
            page: Optional[int], defaults to None
        
        Returns:
          List[dict]
        """

        list_reports = {}
        if community_id is not None:
            list_reports["community_id"] = community_id
        if unresolved_only is not None:
            list_reports['unresolved_only'] = unresolved_only
        if limit is not None:
            list_reports["limit"] = limit
        if page is not None:
            list_reports["page"] = page

        if data := self._requestor.api(Request.GET, "/post/report/list", params=list_reports):
            return data["post_reports"]
        return []

    def resolve_report(self, report_id: int) -> Optional[dict]:
        """
        Resolve a post report

        https://github.com/LemmyNet/lemmy/blob/main/crates/api_common/src/post.rs#L202
        
        Args:
            report_id: int
        Returns:
            Optional[dict]
        """
        return self._requestor.api(
            Request.PUT,
            "/post/report/resolve",
            json={
                "report_id": report_id,
                "resolved": True
            })

    def purge(self, id: int, reason: Optional[str]) -> Optional[dict]:
        """
        Admin purge / delete a post from the database

        Args:
            id (int)
            reason (Optional[str]): Defaults to None

        Returns:
            Optional[dict]: purge result if successful
        """
        purge_post: dict[str, Any] = {
            "post_id": id,
        }
        if reason is not None:
            purge_post["reason"] = reason

        return self._requestor.api(Request.POST, "/admin/purge/post", json=purge_post)

    __call__ = create
