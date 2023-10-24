from typing import Any, List, Literal, Optional, Union
from datetime import datetime
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

    def purge(
            self, 
            id: int,  # FIXME: why is this different? It should be person_id
            reason: Optional[str] = None
        ) -> Optional[dict]:
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
    
    def ban(
            self, 
            ban: bool = True, 
            expires: Optional[Union[datetime, int]] = None, 
            person_id: int = None,
            reason: Optional[str] = None, 
            remove_data: Optional[bool] = None
        ) -> Optional[dict]:
        """
        Admin/Mod ban person from instance

        Args:
            ban (bool): Defaults to True. False Unbans the user
            expires (Optional[Union[datetime, int]]): Unix time of ban expiration as an integer or a datetime object. Defaults to None for permanent ban.
            person_id (int): Defaults to None
            reason (Optional[str]): Defaults to None
            remove_data (Optional[bool]): Defaults to None 
        
        """
        user_ban: dict[str, Any] = {"ban": ban, "person_id": person_id}

        if expires is not None:
            if isinstance(expires, datetime):
                # Convert the datetime to Unix time
                expires = int(expires.timestamp())
            user_ban["expires"] = expires
        if reason is not None:
            user_ban["reason"] = reason
        if remove_data is not None:
            user_ban["remove_data"] = remove_data

        return self._requestor.api(Request.POST, "/user/ban", json=user_ban)