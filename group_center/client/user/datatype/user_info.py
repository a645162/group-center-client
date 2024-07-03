from typing import List

from group_center.client.user. \
    datatype.linux_user import LinuxUserJava
from group_center.client.user. \
    datatype.webhook import AllWebHookUser


class UserInfo:
    name: str = ""
    name_eng: str = ""
    keywords: List[str]
    year: int = 0

    linux_user: LinuxUserJava
    webhook: AllWebHookUser

    def __init__(self):
        self.keywords = []
        self.linux_user = LinuxUserJava()
        self.webhook = AllWebHookUser()

    def from_dict(self, dict_data: dict):
        self.name = dict_data["name"]
        self.name_eng = dict_data["nameEng"]
        self.keywords = dict_data["keywords"]
        self.year = dict_data["year"]

        self.linux_user.from_dict(dict_data["linuxUser"])

    @property
    def home_dir(self):
        return f"/home/{self.name_eng}"


def get_user_info_list(user_list: List[dict]) -> List[UserInfo]:
    final_list = []

    for user_dict in user_list:
        user_info = UserInfo()
        user_info.from_dict(user_dict)

        final_list.append(user_info)

    return final_list
