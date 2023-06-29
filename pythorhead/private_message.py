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
        limit: int
    ) -> Optional[dict]:
        """
        List private messages
        
        Args:
            unread_only (bool).
            page (int).
            limit (int).
            
        Returns:
            dict? private message response
        """
        json: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != "self"}
        params = {"auth": self._requestor.get_auth_token()}
        
        return self._requestor.api(Request.GET, "/private_message/list", params=params, json=json)
