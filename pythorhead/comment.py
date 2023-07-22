from typing import Any, List, Literal, Optional, Union

from pythorhead.requestor import Request, Requestor
from pythorhead.types import CommentSortType, LanguageType, ListingType


class Comment:
    def __init__(self, _requestor: Requestor):
        self._requestor = _requestor

    def list(  # noqa: A003
        self,
        community_id: Optional[int] = None,
        community_name: Optional[str] = None,
        limit: Optional[int] = None,
        max_depth: Optional[int] = None,
        page: Optional[int] = None,
        parent_id: Optional[int] = None,
        post_id: Optional[int] = None,
        saved_only: Optional[bool] = None,
        sort: Optional[CommentSortType] = None,
        type_: Optional[ListingType] = None,
    ) -> List[dict]:
        """

        Get comments, with various filters.

        Args:
            community_id (Optional[int], optional): Defaults to None.
            community_name (Optional[str], optional): Defaults to None.
            limit (Optional[int], optional): Defaults to None.
            max_depth (Optional[int], optional): Defaults to None.
            page (Optional[int], optional): Defaults to None.
            parent_id (Optional[int], optional): Defaults to None.
            post_id (Optional[int], optional): Defaults to None.
            saved_only (Optional[bool], optional): Defaults to None.
            sort (Optional[CommentSortType], optional): Defaults to None.
            type_ (Optional[ListingType], optional): Defaults to None.

        Returns:
            List[dict]: list of comments
        """
        list_comment = {}
        if community_id is not None:
            list_comment["community_id"] = community_id
        if community_name is not None:
            list_comment["community_name"] = community_name
        if limit is not None:
            list_comment["limit"] = limit
        if max_depth is not None:
            list_comment["max_depth"] = max_depth
        if page is not None:
            list_comment["page"] = page
        if parent_id is not None:
            list_comment["parent_id"] = parent_id
        if post_id is not None:
            list_comment["post_id"] = post_id
        if saved_only is not None:
            list_comment["saved_only"] = saved_only
        if sort is not None:
            list_comment["sort"] = sort.value
        if type_ is not None:
            list_comment["type_"] = type_.value

        if data := self._requestor.api(Request.GET, "/comment/list", params=list_comment):
            return data["comments"]
        return []

    def create(
        self,
        post_id: int,
        content: str,
        form_id: Optional[str] = None,
        parent_id: Optional[int] = None,
        language_id: Union[int, LanguageType, None] = None,
    ) -> Optional[dict]:
        """
        Create a comment.

        Args:
            post_id (int)
            content (str)
            form_id (Optional[int], optional): Defaults to None.
            parent_id (Optional[int], optional): Defaults to None.
            language_id (Union[int, LanguageType], optional): Defaults to None.

        Returns:
            Optional[dict]: created comment data if successful
        """

        create_comment = {
            "post_id": post_id,
            "content": content,
        }
        if form_id is not None:
            create_comment["form_id"] = form_id
        if parent_id is not None:
            create_comment["parent_id"] = parent_id
        if language_id is not None:
            if isinstance(language_id, LanguageType):
                create_comment["language_id"] = language_id.value
            else:
                create_comment["language_id"] = language_id

        return self._requestor.api(
            Request.POST,
            "/comment",
            json=create_comment,
        )

    def edit(
        self,
        comment_id: int,
        content: Optional[str] = None,
        form_id: Optional[str] = None,
        language_id: Union[int, LanguageType, None] = None,
    ) -> Optional[dict]:
        """
        Edit a comment.

        Args:
            comment_id (int)
            content (Optional[str], optional): Defaults to None.
            form_id (Optional[str], optional): Defaults to None.
            language_id (Union[int, LanguageType], optional): Defaults to None.

        Returns:
            Optional[dict]: edited comment data if successful
        """
        edit_comment: dict[str, Any] = {
            "comment_id": comment_id,
        }
        if content is not None:
            edit_comment["content"] = content
        if form_id is not None:
            edit_comment["form_id"] = form_id
        if language_id is not None:
            if isinstance(language_id, LanguageType):
                edit_comment["language_id"] = language_id.value
            else:
                edit_comment["language_id"] = language_id

        return self._requestor.api(
            Request.PUT,
            "/comment",
            json=edit_comment,
        )

    def like(self, comment_id: int, score: Literal[-1, 0, 1]) -> Optional[dict]:
        """
        Like / Dislike a comment.

        Args:
            comment_id (int)
            score (int)

        Returns:
            Optional[dict]: like comment data if successful
        """
        return self._requestor.api(
            Request.POST,
            "/comment/like",
            json={
                "comment_id": comment_id,
                "score": score,
            },
        )

    def delete(self, comment_id: int, deleted: bool) -> Optional[dict]:
        """
        Delete / Restore a comment.

        Args:
            comment_id (int): comment_id
            deleted (bool): deleted

        Returns:
            Optional[dict]: deleted comment data if successful
        """
        return self._requestor.api(
            Request.POST,
            "/comment/delete",
            json={
                "comment_id": comment_id,
                "deleted": deleted,
            },
        )

    def distinguish(self, comment_id: int, distinguished: bool) -> Optional[dict]:
        """
        Moderator mark / unmark as a moderator comment.
        Args:
            comment_id (int)
            distinguished (bool)

        Returns:
            Optional[dict]: distinguished comment data if successful
        """

        return self._requestor.api(
            Request.POST,
            "/comment/distinguish",
            json={
                "comment_id": comment_id,
                "distinguished": distinguished,
            },
        )

    def remove(self, comment_id: int, removed: bool, reason: Optional[str] = None) -> Optional[dict]:
        """
        Moderator remove / restore a comment.

        Args:
            comment_id (int)
            removed (bool)
            reason (str, optional): Defaults to None.

        Returns:
            Optional[dict]: removed comment data if successful
        """

        remove_comment = {
            "comment_id": comment_id,
            "removed": removed,
        }

        if reason is not None:
            remove_comment["reason"] = reason

        return self._requestor.api(
            Request.POST,
            "/comment/remove",
            json=remove_comment,
        )

    def report_list(
            self,
            community_id: Optional[int] = None,
            limit: Optional[int] = None,
            page: Optional[int] = None,
            unresolved_only: Optional[bool] = None,
    ) -> List[dict]:
        """
        Returns a list of reported posts

        Args:
            community_id (int, optional): Defaults to None
            limit (int, optional): Defaults to None
            page (int, optional): Defaults to None
            unresolved_only (bool, optional): Defaults to None
        
        Return:
            List[dict]
        """

        list_reports = {}
        if community_id is not None:
            list_reports["community_id"] = community_id
        if limit is not None:
            list_reports["limit"] = limit
        if page is not None:
            list_reports["page"] = page
        if unresolved_only is not None:
            list_reports['unresolved_only'] = unresolved_only

        if data := self._requestor.api(Request.GET, "/comment/report/list", params=list_reports):
            return data["comment_reports"]
        return []

    def resolve_report(self, report_id: int) -> Optional[dict]:
        """
        Resolve a report
        
        Args:
            report_id (int)
        
        Returns:
            Optional[dict]
            
        """
        return self._requestor.api( 
            Request.PUT,
            "/comment/report/resolve",
            json={
                "report_id": report_id,
                "resolved": True
            })

    def save(self, comment_id: int, save: bool) -> Optional[dict]:
        """
        Add / Remove a comment from saved.

        Args:
            comment_id (int)
            save (bool)

        Returns:
            Optional[dict]: saved comment data if successful

        """
        return self._requestor.api(
            Request.PUT,
            "/comment/save",
            json={
                "comment_id": comment_id,
                "save": save,
            },
        )

    def report(self, comment_id: int, reason: str) -> Optional[dict]:
        """
        Report a comment.

        Args:
            comment_id (int): comment_id
            reason (str): reason

        Returns:
            Optional[dict]: report comment data if successful
        """
        return self._requestor.api(
            Request.POST,
            "/comment/report",
            json={
                "comment_id": comment_id,
                "reason": reason,
            },
        )

    def mark_as_read(self, comment_reply_id: int, read: bool) -> Optional[dict]:
        """

        Mark a comment as read

        Args:
            comment_reply_id (int)
            read (bool)

        Returns:
            Optional[dict]: comment data if successful
        """

        mark_as_read_comment = {
            "comment_reply_id": comment_reply_id,
            "read": read,
        }
        return self._requestor.api(Request.POST, "/comment/mark_as_read", json=mark_as_read_comment)

    def purge(self, id: int, reason: Optional[str] = None) -> Optional[dict]:
        """
        Admin purge / delete a comment from the database

        Args:
            id (int)
            reason (Optional[str]): Defaults to None

        Returns:
            Optional[dict]: purge result if successful
        """

        purge_comment: dict[str, Any] = {
            "comment_id": id,
        }

        if reason is not None:
            purge_comment["reason"] = reason

        return self._requestor.api(Request.POST, "/admin/purge/comment", json=purge_comment)

    __call__ = create
