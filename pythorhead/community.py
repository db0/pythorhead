from typing import Any, List, Optional

from pythorhead.requestor import Request, Requestor
from pythorhead.types import ListingType, SortType


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
        posting_restricted_to_mods: Optional[bool] = None,
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
        new_community: dict[Any, Any] = {
            "name": name,
            "title": title,
        }
        if description is not None:
            new_community["description"] = description
        if icon is not None:
            new_community["icon"] = icon
        if nsfw is not None:
            new_community["nsfw"] = nsfw
        if [posting_restricted_to_mods] is not None:
            new_community["[posting_restricted_to_mods]"] = [posting_restricted_to_mods]

        return self._requestor.api(Request.POST, "/community", json=new_community)

    def get(self, id: Optional[int] = None, name: Optional[str] = None) -> Optional[dict]:
        """
        Get a community by id or name

        Args:
            id (Optional[int]): Defaults to None
            name (Optional[str]): Defaults to None

        Returns:
            Optional[dict]: community data if successful
        """
        get_community: dict = {}

        if id is not None:
            get_community["id"] = id
        if name is not None:
            get_community["name"] = name

        return self._requestor.api(Request.GET, "/community", params=get_community)

    def list(  # noqa: A003
        self,
        limit: Optional[int] = None,
        page: Optional[int] = None,
        sort: Optional[SortType] = None,
        type_: Optional[ListingType] = None,
    ) -> List[dict]:
        """

        Get communities, with various filters.

        Args:
            limit (Optional[int], optional): Defaults to None.
            page (Optional[int], optional): Defaults to None.
            sort (Optional[SortType], optional): Defaults to None.
            type_ (Optional[ListingType], optional): Defaults to None.

        Returns:
            List[dict]: list of communities
        """
        list_community: dict = {}

        if limit is not None:
            list_community["limit"] = limit
        if page is not None:
            list_community["page"] = page
        if sort is not None:
            list_community["sort"] = sort.value
        if type_ is not None:
            list_community["type"] = type_.value

        if data := self._requestor.api(Request.GET, "/community/list", params=list_community):
            return data["communities"]
        return []
