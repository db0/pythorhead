from typing import Optional

from pythorhead.requestor import Requestor, Request


class Community:
    def __init__(self, _requestor: Requestor):
        self._requestor = _requestor

    def create(
            self,
            name: str,
            title: str,
            description: Optional[str] = None,
            icon: Optional[str] = None,
            nsfw: Optional[bool] = None,
            posting_restricted_to_mods: Optional[bool] = None
    ) -> Optional[dict]:
        """
        Create a community

        Args:
            name (str)
            title (str)
            description (str, optional): Defaults to None
            icon (str, optional): Defaults to None
            nsfw (bool, optional): Defaults to None
            posting_restricted_to_mods (bool, optional): Defaults to None

        Returns:
            Optional[dict]: post data if successful
        """
        new_community = {
            "name": name,
            "title": title,

        }
        if description is not None:
            new_community['description'] = description
        if icon is not None:
            new_community['icon'] = icon
        if nsfw is not None:
            new_community['nsfw'] = nsfw
        if [posting_restricted_to_mods] is not None:
            new_community['[posting_restricted_to_mods]'] = [posting_restricted_to_mods]

        return self._requestor.api(Request.POST, "/post", json=new_community)
