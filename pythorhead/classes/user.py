from dataclasses import dataclass, asdict
from datetime import datetime
from dateutil import parser
from pythorhead.utils import json_serializer

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
    comments: list[dict] = None
    posts: list[dict] = None
    # The owning lemmy instance. We use it to reach the API classes
    lemmy = None
    
    @classmethod
    def from_dict(cls, person_dict: dict, lemmy) -> 'LemmyUser':
        # Convert string to datetime for ban_expires if it exists
        for key in {'ban_expires', 'updates', 'published'}:
            if key in person_dict and person_dict[key]:
                person_dict[key] = parser.isoparse(person_dict[key])
        new_user = cls(**person_dict)
        new_user.lemmy = lemmy
        return new_user
    
    def refresh(self) -> None:
        """
        Update instance attributes from a new dictionary while preserving custom fields.
        
        Args:
            new_data: Dictionary containing updated user data
        """
        fresh_data = self.lemmy.user.get(person_id=self.id)
        user_dict = fresh_data['person_view']['person']
        user_dict['is_admin'] = fresh_data['person_view']['is_admin']
        user_dict['comments'] = fresh_data['comments']
        user_dict['posts'] = fresh_data['posts']
        # Handle datetime conversion
        if 'ban_expires' in user_dict and user_dict['ban_expires']:
            user_dict['ban_expires'] = datetime.fromisoformat(user_dict['ban_expires'])
        
        for field_name in user_dict:
            setattr(self, field_name, user_dict[field_name])


    def purge(self) -> None:
        self.lemmy.user.purge(person_id=self.person_id)
    
    def ban(self,
            ban: bool = True, 
            expires: datetime | int | None = None, 
            reason: str | None = None, 
            remove_data: bool | None = None
        ) -> None:
        self.lemmy.user.ban(
            person_id=self.person_id,
            ban = ban,
            expires = expires,
            reason = reason,
            remove_data = remove_data,
        )
        self.refresh()
    
    def update(self):
        if self.lemmy.user._requestor.logged_in_username != self.name:
            raise Exception("Cannot update user details for anyone but the currently logged-in user.")
        self.lemmy.user.save_user_settings(
            avatar=self.avatar,
            banner=self.banner,
            display_name=self.display_name,
            bio=self.bio,
            matrix_user_id=self.matrix_user_id,
            bot_account=self.bot_account,
        )
        self.refresh()
    
    def set_settings(self, **kwargs):
        if self.lemmy.user._requestor.logged_in_username != self.name:
            raise Exception("Cannot update user settings for anyone but the currently logged-in user.")
        self.lemmy.user.save_user_settings(**kwargs)
        self.refresh()

    def asdict(self):
        return asdict(self)

    def asjson(self, indent=4):      
        selfdict = self.asdict()
        return json.dumps(selfdict, indent=indent, default=json_serializer)
    
    def pm(self, content):
        self.lemmy.private_message(
            content=content,
            recipient_id=self.id,
        )
    
    def get_latest_posts(self):
        self.refresh()
        return self.posts

    def get_latest_comments(self):
        self.refresh()
        return self.comments
    