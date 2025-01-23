from typing import Any, List, Optional, Union

from pythorhead.requestor import Request, Requestor
from pythorhead.types import ModlogActionType


class Modlog:
    def __init__(self, _requestor: Requestor):
        self._requestor = _requestor

    def get(
        self,
        comment_id: Optional[int] = None,
        community_id: Optional[int] = None,
        limit: Optional[int] = None,
        mod_person_id: Optional[int] = None,
        other_person_id: Optional[int] = None,
        page: Optional[int] = None,
        post_id: Optional[int] = None,
        type_: Optional[ModlogActionType] = None
    ) -> Optional[dict]:
        """

        Get Modlog

        Args:
            comment_id (int, optional): Defaults to None.
            community_id (int, optional): Defaults to None.
            limit (int, optional): Defaults to None.
            mod_person_id (int, optional): Defaults to None.
            other_person_id (int, optional): Defaults to None.
            page (int, optional): Defaults to None.
            post_id (int, optional): Defaults to None.
            type_ (ModlogActionType, optional): Defaults to None.
        Returns:
            Optional[dict]: post data if successful
        """

        params: dict[str, Any] = {
            key: value for key, value in locals().items() if value is not None and key != "self"
        }

        return self._requestor.api(Request.GET, "/modlog", params=params)
