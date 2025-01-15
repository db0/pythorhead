from typing import Any, List, Optional, Union

from pythorhead.requestor import Request, Requestor
from pythorhead.types import ListingType, LanguageType


class Emoji:
    def __init__(self, _requestor: Requestor):
        self._requestor = _requestor

    def get(
        self,
    ) -> Optional[dict]:
        """
        Get a list of all defined custom emoji

        Returns:
            dict: emoji view
        """
        return self._requestor.api(Request.GET, "/site")["custom_emojis"]
    
    # FIXME: untested
    def edit(
            self, 
            emoji_id: int, 
            category: str, 
            image_url: str,
            alt_text: str, 
            keywords: str,
        ) -> dict:
        """
        Admin/Mod Edit an existing custom emoji

        Args:
            emoji_id (int): The ID of the emoji to edit
            category (str): The category of the emoji
            image_url (str): The URL of the emoji image
            alt_text (str): The alt text for the emoji
            keywords (str): The keywords associated with the emoji

        Returns:
          dict: The edited emoji view
        """
        emoji_data = {
          "id": emoji_id,
          "category": category,
          "image_url": image_url,
          "alt_text": alt_text,
          "keywords": keywords,
        }

        return self._requestor.api(Request.PUT, f"/custom_emoji", json=emoji_data)
    
    # FIXME: untested
    def create(
            self, 
            emoji_id: int, 
            category: str, 
            image_url: str,
            alt_text: str, 
            keywords: str,
        ) -> dict:
        """
        Admin/Mod Create a new custom emoji

        Args:
            if (int): The ID of the emoji to edit
            category (str): The category of the emoji
            image_url (str): The URL of the emoji image
            alt_text (str): The alt text for the emoji
            keywords (str): The keywords associated with the emoji

        Returns:
          dict: The edited emoji view
        """
        emoji_data = {
          "id": emoji_id,
          "category": category,
          "image_url": image_url,
          "alt_text": alt_text,
          "keywords": keywords,
        }

        return self._requestor.api(Request.POST, f"/custom_emoji", json=emoji_data)
    
    # FIXME: untested
    def delete(
            self, 
            emoji_id: int, 
        ) -> bool:
        """
        Admin/Mod delete an existing custom emoji

        Args:
            emoji_id (int): The ID of the emoji to edit

        Returns:
          True if the emoji was deleted successfully. Else false.
        """
        emoji_data = {
          "id": emoji_id,
        }

        return self._requestor.api(Request.POST, f"/custom_emoji/delete", json=emoji_data) == 'OK'
