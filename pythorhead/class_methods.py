from pythorhead.classes.admin import LemmyRegistrationApplication, LemmyLocalUser
from pythorhead.classes.user import LemmyUser

def get_user(lemmy, **kwargs) -> LemmyUser | None:
    return_json = lemmy.user.get(**kwargs)
    if return_json is None:
        return
    data_dict = return_json['person_view']['person']
    data_dict['is_admin'] = return_json['person_view']['is_admin']
    data_dict['comments'] = return_json['comments']
    data_dict['posts'] = return_json['posts']
    return LemmyUser.from_dict(data_dict, lemmy)

def get_applications(lemmy, **kwargs) -> list[LemmyRegistrationApplication]:
    return_json = lemmy.admin.list_applications(**kwargs)
    regapps = []
    if return_json is None:
        return regapps
    for data in return_json["registration_applications"]:
        data_dict = data["registration_application"]
        data_dict["creator_local_user"] = LemmyLocalUser.from_dict(data["creator_local_user"], lemmy)
        data_dict["creator"] = LemmyUser.from_dict(data["creator"], lemmy)
        data_dict["admin"] = None
        if data.get("admin"):
            admin_dict = data["admin"]
            admin_dict["is_admin"] = True
            data_dict["admin"] = LemmyUser.from_dict(admin_dict, lemmy)
        regapps.append(LemmyRegistrationApplication.from_dict(data_dict, lemmy))
    return regapps