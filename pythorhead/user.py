from typing import Any, List, Literal, Optional

from pythorhead.requestor import Request, Requestor
from pythorhead.types import SortType


class User:
    def __init__(self, _requestor: Requestor):
        self._requestor = _requestor

    def get(
        self,
        person_id: Optional[str] = None,
        username: Optional[str] = None,
        sort: Optional[SortType] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        community_id: Optional[int] = None,
        saved_only: Optional[bool] = None,
    ) -> Optional[dict]:
        """
        Get user details with various filters.

        Args:
            person_id (Optional[str], optional): Defaults to None.
            username (Optional[str], optional): Defaults to None.
            sort (Optional[CommentSortType], optional): Defaults to None.
            page (Optional[int], optional): Defaults to None.
            limit (Optional[int], optional): Defaults to None.
            community_id (Optional[int], optional): Defaults to None.
            saved_only (Optional[bool], optional): Defaults to None.
        Returns:
            dict: user view
        """
        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != "self"}
        return self._requestor.api(Request.GET, "/user", params=params)

    def purge(self, id: int, reason: Optional[str] = None) -> Optional[dict]:
        """
        Admin purge / delete a person from the database

        Args:
            id (int)
            reason (Optional[str]): Defaults to None

        Returns:
            Optional[dict]: purge result if successful
        """

        user_purge: dict[str, Any] = {"person_id": id}

        if reason is not None:
            user_purge["reason"] = reason

        return self._requestor.api(Request.POST, "/admin/purge/person", json=user_purge)
