from enum import Enum


class SortType(str, Enum):
    Hot = "Hot"
    New = "New"
    Old = "Old"
    Active = "Active"
    TopAll = "TopAll"
    TopDay = "TopDay"
    TopWeek = "TopWeek"
    TopMonth = "TopMonth"
    TopYear = "TopYear"
    TopHour = "TopHour"
    TopSixHour = "TopSixHour"
    TopTwelveHour = "TopTwelveHour"
    NewComments = "NewComments"
    MostComments = "MostComments"


class CommentSortType(str, Enum):
    Hot = "Hot"
    New = "New"
    Old = "Old"
    Top = "Top"
