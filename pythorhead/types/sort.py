from enum import Enum


class SortType(Enum):
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


class CommentSortType(Enum):
    Hot = "Hot"
    New = "New"
    Old = "Old"
    Top = "Top"
