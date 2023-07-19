from enum import Enum


class ListingType(str, Enum):
    All = "All"
    Community = "Community"
    Local = "Local"
    Subscribed = "Subscribed"
