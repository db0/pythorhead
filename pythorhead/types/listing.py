from enum import Enum


class ListingType(str, Enum):
    All = "All"
    Community = "Community"
    Local = "Local"
    Subscribed = "Subscribed"
    ModeratorView = "ModeratorView"

class PostListingType(str, Enum):
    All = "All"
    Community = "Community"
    Local = "Local"
    Subscribed = "Subscribed"
    ModeratorView = "ModeratorView"