from enum import Enum


class SearchOption(str, Enum):
    No = "No"
    Yes = "Yes"
    #  A retry search means wait a bit for the instance to get the federated results and retry the search
    Retry = "Retry"

class SearchType(str, Enum):
    All = "All"
    Comments = "Comments"
    Posts = "Posts"
    Communities = "Communities"
    Users = "Users"
    Url = "Url"
