from enum import Enum


class ModlogActionType(str, Enum):
    All = "All"
    ModRemovePost = "ModRemovePost"
    ModLockPost = "ModLockPost"
    ModFeaturePost = "ModFeaturePost"
    ModRemoveComment = "ModRemoveComment"
    ModRemoveCommunity = "ModRemoveCommunity"
    ModBanFromCommunity = "ModBanFromCommunity"
    ModAddCommunity = "ModAddCommunity"
    ModTransferCommunity = "ModTransferCommunity"
    ModAdd = "ModAdd"
    ModBan = "ModBan"
    ModHideCommunity = "ModHideCommunity"
    AdminPurgePerson = "AdminPurgePerson"
    AdminPurgeCommunity = "AdminPurgeCommunity"
    AdminPurgePost = "AdminPurgePost"
    AdminPurgeComment = "AdminPurgeComment"
