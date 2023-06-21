from typing import Any, List, Literal, Optional

from pythorhead.requestor import Request


class PrivateMessage:
    def __init__(self,_requestor):
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
        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != 'self'}
        return self._requestor.request(Request.POST, "/private_message", json=params)

    __call__ = create