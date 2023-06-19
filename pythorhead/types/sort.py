from enum import Enum


class PostSortType(Enum):
    Active = "Active"
    Hot = "Hot"
    MostComments = "MostComments"
    New = "New"
    Old = "Old"
    TopAll = "TopAll"
    TopDay = "TopDay"
    TopMonth = "TopMonth"
    TopWeek = "TopWeek"
    TopYear = "TopYear"


class CommentSortType(Enum):
    Hot = "Hot"
    New = "New"
    Old = "Old"
    Top = "Top"
