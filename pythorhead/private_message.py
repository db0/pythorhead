from typing import Any, Optional

from pythorhead.requestor import Request, Requestor


class PrivateMessage:
    def __init__(self, _requestor: Requestor):
        self._requestor = _requestor

    def create(
        self,
        content: str,
        recipient_id: str,
    ) -> Optional[dict]:
        """
        Send a private message

        Args:
            content (str).
            recipient_id (int).
        Returns:
            dict: private message response
        """
        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != "self"}
        return self._requestor.api(Request.POST, "/private_message", json=params)

    __call__ = create
    
    def list(
        self,
        unread_only: bool,
        page: int,
        limit: int = 20
    ) -> Optional[dict]:
        """
        List private messages
        
        Args:
            unread_only (bool).
            page (int).
            limit (int) with a max of 50, defaults to 20.
            
        Returns:
            dict? private message response
        """
        limit = 50 if limit > 50 else limit
        unread_only = 'true' if unread_only else 'false'
        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != "self"}
        return self._requestor.api(Request.GET, "/private_message/list",  params=params)
