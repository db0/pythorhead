from enum import Enum


class ListingType(Enum):
    All = "All"
    Community = "Community"
    Local = "Local"
    Subscribed = "Subscribed"

    def __str__(self):
        return self.value
