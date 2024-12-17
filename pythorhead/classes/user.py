from typing import Any, List, Literal, Optional, Union
from dataclasses import dataclass
from datetime import datetime
from pythorhead import lemmy
from pythorhead.types import SortType, ListingType, LanguageType


@dataclass
class LemmyUser:
    id: int
    name: str
    avatar: str
    banned: bool
    published: str
    updated: str
    actor_id: str
    bio: str
    local: bool
    banner: str
    deleted: bool
    matirx_user_id: str
    bot_account: bool
    ban_expires: datetime
    instance_id: int
    is_admin: bool

    user_request_class = None
    
    @classmethod
    def from_dict(cls, person_dict: dict, user_request_class) -> 'LemmyUser':
        # Convert string to datetime for ban_expires if it exists
        if 'ban_expires' in person_dict and person_dict['ban_expires']:
            person_dict['ban_expires'] = datetime.fromisoformat(person_dict['ban_expires'])
        
        return cls(**person_dict, user_request_class)
    
    def refresh(self) -> None:
        """
        Update instance attributes from a new dictionary while preserving custom fields.
        
        Args:
            new_data: Dictionary containing updated user data
        """
        new_data = self.user_request_class.get(person_id=self.person_id)
        # Handle datetime conversion
        if 'ban_expires' in new_data and new_data['ban_expires']:
            new_data['ban_expires'] = datetime.fromisoformat(new_data['ban_expires'])
        
        for field_name in new_data:
            setattr(self, field_name, new_data[field_name])


    def purge(self) -> None:
        self.user_request_class.purge(person_id=self.person_id)
    
    def ban(self,
            ban: bool = True, 
            expires: datetime | int | None = None, 
            reason: str | None = None, 
            remove_data: bool | None = None
        ) -> None:
        self.user_request_class.ban(
            person_id=self.person_id,
            ban = ban,
            expires = expires,
            reason = reason,
            remove_data = remove_data,
        )
        self.refresh()
    
    def update(self):
        if self.user_request_class._requestor.logged_in_username != self.name:
            raise Exception("Cannot update user details for anyone but the currently logged-in user.")
        self.user_request_class.save_user_settings(
            avatar=self.avatar,
            banner=self.banner,
            display_name=self.name,
            bio=self.bio,
            matrix_user_id=self.matrix_user_id,
            bot_account=self.bot_account,
        )
        self.refresh()
    
    def set_settings(self, **kwargs):
        if self.user_request_class._requestor.logged_in_username != self.name:
            raise Exception("Cannot update user settings for anyone but the currently logged-in user.")
        self.user_request_class.save_user_settings(**kwargs)
        self.refresh()
