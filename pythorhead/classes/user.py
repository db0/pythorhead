from datetime import datetime
from dateutil import parser
from pythorhead.classes.base import LemmyBaseClass
from dataclasses import dataclass

@dataclass
class LemmyUser(LemmyBaseClass):
    id: int
    name: str
    banned: bool
    published: datetime
    actor_id: str
    local: bool
    deleted: bool
    bot_account: bool
    instance_id: int
    is_admin: bool = False
    display_name: str | None = None
    bio: str | None = None
    avatar: str | None = None
    banner: str | None = None
    matrix_user_id: str | None = None
    ban_expires: datetime | None = None
    updated: datetime | None = None
    #TODO Convert to classes
    comments: list[dict] = None
    posts: list[dict] = None
    
    @classmethod
    def from_dict(cls, data_dict: dict, lemmy) -> 'LemmyUser':
        # Convert string to datetime for ban_expires if it exists
        
        for key in {'ban_expires', 'updates', 'published'}:
            if key in data_dict and data_dict[key]:
                data_dict[key] = parser.isoparse(data_dict[key])
        new_class = cls(**data_dict)
        new_class._lemmy = lemmy
        new_class._origin = data_dict
        return new_class
    
    def refresh(self) -> None:
        """
        Update instance attributes from a new dictionary while preserving custom fields.
        
        Args:
            new_data: Dictionary containing updated user data
        """
        fresh_data = self._lemmy.user.get(person_id=self.id)
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
        self._lemmy.user.purge(person_id=self.person_id)
    
    def ban(self,
            ban: bool = True, 
            expires: datetime | int | None = None, 
            reason: str | None = None, 
            remove_data: bool | None = None
        ) -> None:
        self._lemmy.user.ban(
            person_id=self.person_id,
            ban = ban,
            expires = expires,
            reason = reason,
            remove_data = remove_data,
        )
        self.refresh()
    
    def update(self):
        if self._lemmy.user._requestor.logged_in_username != self.name:
            raise Exception("Cannot update user details for anyone but the currently logged-in user.")
        self._lemmy.user.save_user_settings(
            avatar=self.avatar,
            banner=self.banner,
            display_name=self.display_name,
            bio=self.bio,
            matrix_user_id=self.matrix_user_id,
            bot_account=self.bot_account,
        )
        self.refresh()
    
    def set_settings(self, **kwargs):
        if self._lemmy.user._requestor.logged_in_username != self.name:
            raise Exception("Cannot update user settings for anyone but the currently logged-in user.")
        self._lemmy.user.save_user_settings(**kwargs)
        self.refresh()
    
    def pm(self, content):
        self._lemmy.private_message(
            content=content,
            recipient_id=self.id,
        )
    
    def get_latest_posts(self):
        self.refresh()
        return self.posts

    def get_latest_comments(self):
        self.refresh()
        return self.comments
    