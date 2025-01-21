from datetime import datetime
from dateutil import parser
from pythorhead.classes.base import LemmyBaseClass
from pythorhead.classes.user import LemmyUser
from dataclasses import dataclass
from pythorhead.types import SortType, ListingType, LanguageType
from enum import Enum

# TODO: Convert to StrEnum in python 3.11
class ApplicationStatus(str, Enum):
    Pending = "pending"
    Accepted = "accepted"
    Denied = "denied"


@dataclass
class LemmyLocalUser(LemmyBaseClass):
    id: int
    person_id: int
    email: str
    show_nsfw: bool
    theme: str
    default_sort_type: SortType
    default_listing_type: ListingType
    interface_language: LanguageType
    show_avatars: bool
    send_notifications_to_email: bool
    show_scores: bool
    show_bot_accounts: bool
    show_read_posts: bool
    email_verified: bool
    accepted_application: bool
    open_links_in_new_tab: bool
    blur_nsfw: bool
    auto_expand: bool
    infinite_scroll_enabled: bool
    admin: bool
    post_listing_mode: str
    totp_2fa_enabled: bool
    enable_keyboard_navigation: bool
    enable_animated_images: bool
    collapse_bot_comments: bool
    published: datetime | None = None
    
    @classmethod
    def from_dict(cls, data_dict: dict, lemmy) -> 'LemmyRegistrationApplication':
        # Convert string to datetime for ban_expires if it exists
        for key in {'published'}:
            if key in data_dict and data_dict[key]:
                data_dict[key] = parser.isoparse(data_dict[key])
        for key in {'default_sort_type','default_listing_type'}:
            if key in data_dict and data_dict[key]:
              data_dict[key] = cls.__annotations__[key](data_dict[key])
        for key in {'interface_language'}:
            if key in data_dict and data_dict[key]:
              data_dict[key] = cls.__annotations__[key][data_dict[key].upper()]
        new_class = cls(**data_dict)
        new_class._lemmy = lemmy
        new_class._origin = data_dict        
        return new_class



@dataclass
class LemmyRegistrationApplication(LemmyBaseClass):
    id: int
    local_user_id: int
    answer: str
    published: datetime
    creator_local_user: dict
    creator: LemmyUser
    creator_local_user: LemmyLocalUser
    creator: LemmyUser
    admin_id: int | None = None
    deny_reason: str | None = None
    admin: LemmyUser | None = None
    
    
    @classmethod
    def from_dict(cls, data_dict: dict, lemmy) -> 'LemmyRegistrationApplication':
        # Convert string to datetime for ban_expires if it exists
        for key in {'published'}:
            if key in data_dict and data_dict[key]:
                data_dict[key] = parser.isoparse(data_dict[key])
        new_class = cls(**data_dict)
        new_class._lemmy = lemmy
        new_class._origin = data_dict        
        return new_class

    def get_application_status(self) -> str:
        if self.creator_local_user.accepted_application:
            return ApplicationStatus.Accepted
        elif self.deny_reason:
            return ApplicationStatus.Denied
        return ApplicationStatus.Pending