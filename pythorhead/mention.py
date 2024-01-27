from typing import Any, Optional
from pythorhead.requestor import Request, Requestor
from pythorhead.types import SortType


class Mention:
    def __init__(self, _requestor: Requestor):
        self._requestor = _requestor

    def list(
        self,
        unread_only: bool,
        sort: Optional[SortType] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Optional[dict]:
        """
        List all user mentions

        Args: 
            unread_only (bool).
            sort? (SortType)
            page? (int).
            limit? (int)

        Returns:
            dict? mentions response
        """
        unread_only = 'true' if unread_only else 'false'
    
        params: dict[str, Any] = {key: value for key, value in locals(
        ).items() if value is not None and key != "self"}
        return self._requestor.api(Request.GET, "/user/mention", params=params)

    def mark_as_read(self, person_mention_id: int, read: bool) -> Optional[dict]:
        """

        Mark a mention as read

        Args:
            person_mention_id (int)
            read (bool)

        Returns:
            Optional[dict]: comment data if successful
        """

        mark_as_read_mention = {
            "person_mention_id": person_mention_id,
            "read": read,
        }
        return self._requestor.api(Request.POST, "/user/mention/mark_as_read", json=mark_as_read_mention)
