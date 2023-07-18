from typing import Any, List, Optional, Union

from pythorhead.requestor import Request, Requestor
from pythorhead.types import LanguageType, ListingType, SortType


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
        discussion_languages: Optional[List[Union[int, LanguageType]]] = None,
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
            discussion_languages: (List[Union[int, LanguageType]], optional): Defaults to None

        Returns:
            Optional[dict]: post data if successful
        """
        new_community: dict[str, Any] = {
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
        if discussion_languages is not None:
            new_community["discussion_languages"] = [
                language.value for language in discussion_languages if isinstance(language, LanguageType)
            ]

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

        params: list[str, Any] = {key: value for key, value in locals().items() if value is not None and key != "self"}
        if data := self._requestor.api(Request.GET, "/community/list", params=params):
            return data["communities"]
        return []

    def follow(self, id: int, follow: Optional[bool] = True):
        """

        Subscribe to the community with supplied id.
        Args:
            id (int)
            follow (Optional[bool], optional): Defaults to True

        Returns:
            Optional[dict]: community info if successful

        """

        follow_community: dict = {}
        follow_community["community_id"] = id
        follow_community["follow"] = follow

        if data := self._requestor.api(Request.POST, "/community/follow", json=follow_community):
            return data["community_view"]
        return None

    def purge(self, id: int, reason: Optional[str] = None) -> Optional[dict]:
        """
        Admin  purge / delete a community from the database

        Args:
            id (int)
            reason (Optional[str]): Defaults to None

        Returns:
            Optional[dict]: purge result if successful
        """

        purge_community: dict[str, Any] = {
            "community_id": id,
        }

        if reason is not None:
            purge_community["reason"] = reason

        return self._requestor.api(Request.POST, "/admin/purge/community", json=purge_community)
        
    def add_mod_to_community(self, added: bool, community_id: int, person_id: int) -> Optional[dict]:
        """

        Add a mod to community

        Args:
            added (bool)
            community_id (int)
            person_id (bool)

        Returns:
            Optional[dict]: 
        """

        addmodtocommunity = {
            "added": added,
            "community_id": community_id,
            "person_id": person_id
        }
        return self._requestor.api(Request.POST, "/community/mod", json=addmodtocommunity)
