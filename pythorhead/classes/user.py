from dataclasses import dataclass, asdict
from datetime import datetime
from pythorhead import lemmy
from pythorhead.types import SortType, ListingType, LanguageType
from dateutil import parser
import json

@dataclass
class LemmyUser:
    id: int
    name: str
    banned: bool
    published: datetime
    actor_id: str
    local: bool
    deleted: bool
    bot_account: bool
    instance_id: int
    is_admin: bool
    display_name: str | None = None
    bio: str | None = None
    avatar: str | None = None
    banner: str | None = None
    matrix_user_id: str | None = None
    ban_expires: datetime | None = None
    updated: datetime | None = None

    user_request_class = None
    
    @classmethod
    def from_dict(cls, person_dict: dict, user_request_class) -> 'LemmyUser':
        # Convert string to datetime for ban_expires if it exists
        for key in {'ban_expires', 'updates', 'published'}:
            if key in person_dict and person_dict[key]:
                person_dict[key] = parser.isoparse(person_dict[key])
        new_user = cls(**person_dict)
        new_user.user_request_class = user_request_class
        return new_user
    
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
            display_name=self.display_name,
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

    def asdict(self):
        return asdict(self)

    def asjson(self, indent=4):
        def custom_serializer(obj):
            if isinstance(obj, datetime):
                return obj.isoformat()  # Convert datetime to ISO 8601 string
            else:
                return obj
            raise TypeError(f"Type {type(obj)} not serializable")
        
        selfdict = self.asdict()
        return json.dumps(selfdict, indent=indent, default=custom_serializer)