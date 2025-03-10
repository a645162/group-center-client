from typing import List

from group_center.client.user.datatype.linux_user import LinuxUserJava
from group_center.client.user.datatype.webhook import AllWebHookUser


class UserInfo:
    """用户信息类 / User information class

    Attributes:
        name (str): 用户名 / User name
        name_eng (str): 英文用户名 / English user name
        keywords (List[str]): 关键词列表 / Keywords list
        year (int): 年份 / Year
        linux_user (LinuxUserJava): Linux 用户信息 / Linux user information
        webhook (AllWebHookUser): Webhook 信息 / Webhook information
    """

    name: str = ""
    name_eng: str = ""
    keywords: List[str]
    year: int = 0

    linux_user: LinuxUserJava
    webhook: AllWebHookUser

    def __init__(self):
        """初始化用户信息 / Initialize user information"""
        self.keywords = []
        self.linux_user = LinuxUserJava()
        self.webhook = AllWebHookUser()

    def from_dict(self, dict_data: dict):
        """从字典加载数据 / Load data from dictionary

        Args:
            dict_data (dict): 包含用户信息的字典 / Dictionary containing user information
        """
        self.name = dict_data["name"]
        self.name_eng = dict_data["nameEng"]
        self.keywords = dict_data["keywords"]
        self.year = dict_data["year"]

        self.linux_user.from_dict(dict_data["linuxUser"])

    @property
    def home_dir(self) -> str:
        """获取用户主目录路径 / Get user home directory path

        Returns:
            str: 用户主目录路径 / User home directory path
        """
        return f"/home/{self.name_eng}"


def get_user_info_list(user_list: List[dict]) -> List[UserInfo]:
    """从用户字典列表获取用户信息列表 / Get user info list from user dictionary list

    Args:
        user_list (List[dict]): 用户字典列表 / User dictionary list

    Returns:
        List[UserInfo]: 用户信息列表 / User information list
    """
    final_list = []

    for user_dict in user_list:
        user_info = UserInfo()
        user_info.from_dict(user_dict)

        final_list.append(user_info)

    return final_list
