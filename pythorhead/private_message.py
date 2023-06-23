from typing import Any, List, Literal, Optional

from pythorhead.requestor import Request


class PrivateMessage:
    def __init__(self,_requestor):
        self._requestor = _requestor

    def create(
        self,
        content: str,
        recipient_id: int,
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

    def delete(
        self,
        deleted: bool,
        private_message_id: int,
    ) -> Optional[dict]:
        """
        Delete a private message.

        Args:
            deleted (bool).
            private_message_id (int).
        Returns:
            dict: private message response
        """
        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != 'self'}
        return self._requestor.request(Request.POST, "/private_message/delete", json=params)

    def list(
        self,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        unread_only: Optional[bool] = None,
    ) -> Optional[dict]:
        """
        Get / fetch private messages.

        Args:
            limit (int).
            page (int).
            unread_only (bool).
        Returns:
            dict: private message response
        """
        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != 'self'}
        return self._requestor.request(Request.GET, "/private_message/list", params=params)

    def delete(
        self,
        deleted: bool,
        private_message_id: int,
    ) -> Optional[dict]:
        """
        Delete a private message.

        Args:
            deleted (bool).
            private_message_id (int).
        Returns:
            dict: private message response
        """
        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != 'self'}
        return self._requestor.request(Request.POST, "/private_message/delete", json=params)

    def mark_as_read(
        self,
        private_message_id: int,
        read: bool,
    ) -> Optional[dict]:
        """
        Mark a private message as read.

        Args:
            private_message_id (int).
            read (bool).
        Returns:
            dict: private message response
        """
        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != 'self'}
        return self._requestor.request(Request.POST, "/private_message/mark_as_read", json=params)

    def report(
        self,
        private_message_id: int,
        reason: str,
    ) -> Optional[dict]:
        """
        Create a report for a private message.

        Args:
            private_message_id (int).
            reason (str).
        Returns:
            dict: private message report response
        """
        params: dict[str, Any] = {key: value for key, value in locals().items() if value is not None and key != 'self'}
        return self._requestor.request(Request.POST, "/private_message/report", json=params)

    __call__ = create
