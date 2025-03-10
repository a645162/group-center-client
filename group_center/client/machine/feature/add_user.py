from typing import List

from group_center.client.user.datatype.user_info import UserInfo
from group_center.user.linux.linux_user import LinuxUser


def get_linux_user_add_text(
    user_name: str,
    password: str,
    uid: int,
    gid: int,
    group_name: str,
    home_dir: str,
    shell: str,
) -> str:
    """生成 Linux 用户添加文本
    Generate Linux user add text

    Args:
        user_name (str): 用户名 | Username
        password (str): 密码 | Password
        uid (int): 用户ID | User ID
        gid (int): 组ID | Group ID
        group_name (str): 组名 | Group name
        home_dir (str): 主目录 | Home directory
        shell (str): 默认shell | Default shell

    Returns:
        str: Linux 用户添加文本 | Linux user add text
    """
    # user001::600:100:user:/home/user001:/bin/bash
    return f"{user_name}:{password}:{uid}:{gid}:{group_name}:{home_dir}:{shell}"


def linux_add_user_txt(user_info_list: List[UserInfo], password: str = "") -> str:
    """生成批量添加 Linux 用户的文本
    Generate text for batch adding Linux users

    Args:
        user_info_list (List[UserInfo]): 用户信息列表 | List of user info
        password (str, optional): 密码 | Password. Defaults to "".

    Returns:
        str: 批量添加用户的文本 | Text for batch adding users
    """
    final_text: str = ""

    for user_info in user_info_list:
        user_name: str = user_info.name_eng

        uid: int = user_info.linux_user.uid
        gid: int = user_info.linux_user.gid

        group_name: str = user_name
        home_dir: str = user_info.home_dir
        shell: str = "/bin/bash"

        final_text += (
            get_linux_user_add_text(
                user_name=user_name,
                password=password,
                uid=uid,
                gid=gid,
                group_name=group_name,
                home_dir=home_dir,
                shell=shell,
            )
            + "\n"
        )

    return final_text.strip()


def create_user(user_info: UserInfo, password: str = "") -> None:
    """创建单个 Linux 用户
    Create a single Linux user

    Args:
        user_info (UserInfo): 用户信息 | User info
        password (str, optional): 密码 | Password. Defaults to "".
    """
    linux_user_obj: LinuxUser = LinuxUser(user_info.name_eng)

    if linux_user_obj.is_exist():
        print(f"User {user_info.name_eng} already exist")
    else:
        if not linux_user_obj.create(password=password):
            print(f"Create user {user_info.name_eng} failed")
            return

    linux_user_obj.uid = user_info.linux_user.uid
    linux_user_obj.gid = user_info.linux_user.gid


def create_linux_users(user_info_list: List[UserInfo], password: str = "") -> None:
    """批量创建 Linux 用户
    Batch create Linux users

    Args:
        user_info_list (List[UserInfo]): 用户信息列表 | List of user info
        password (str, optional): 密码 | Password. Defaults to "".
    """
    for user_info in user_info_list:
        create_user(user_info=user_info, password=password)


def remove_user(user_info: UserInfo) -> None:
    """删除单个 Linux 用户
    Remove a single Linux user

    Args:
        user_info (UserInfo): 用户信息 | User info
    """
    linux_user_obj: LinuxUser = LinuxUser(user_info.name_eng)

    if not linux_user_obj.is_exist():
        print(f"User {user_info.name_eng} not exist")

    if not linux_user_obj.delete():
        print(f"Remove user {user_info.name_eng} failed")


def remove_linux_users(user_info_list: List[UserInfo]) -> None:
    """批量删除 Linux 用户
    Batch remove Linux users

    Args:
        user_info_list (List[UserInfo]): 用户信息列表 | List of user info
    """
    for user_info in user_info_list:
        remove_user(user_info=user_info)


def add_users_to_linux_group(user_info_list: List[UserInfo], group_name: str) -> None:
    """将用户添加到 Linux 组
    Add users to Linux group

    Args:
        user_info_list (List[UserInfo]): 用户信息列表 | List of user info
        group_name (str): 组名 | Group name
    """
    for user_info in user_info_list:
        linux_user_obj: LinuxUser = LinuxUser(user_info.name_eng)
        linux_user_obj.add_to_group(group_name=group_name)
