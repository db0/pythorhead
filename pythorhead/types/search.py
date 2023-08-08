from enum import Enum


class SearchType(str, Enum):
    No = "No"
    Yes = "Yes"
    #  A retry search means wait a bit for the instance to get the federated results and retry the search
    Retry = "Retry"
