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
):
    # user001::600:100:user:/home/user001:/bin/bash
    return f"{user_name}:{password}:{uid}:{gid}:{group_name}:{home_dir}:{shell}"


def linux_add_user_txt(user_info_list: List[UserInfo], password: str = ""):
    final_text = ""

    for user_info in user_info_list:
        user_name: str = user_info.name_eng

        uid: int = user_info.linux_user.uid
        gid: int = user_info.linux_user.gid

        group_name: str = user_name
        home_dir: str = user_info.home_dir
        shell: str = "/bin/bash"

        final_text += get_linux_user_add_text(
            user_name=user_name,
            password=password,
            uid=uid,
            gid=gid,
            group_name=group_name,
            home_dir=home_dir,
            shell=shell,
        ) + "\n"

    return final_text.strip()


def create_user(user_info: UserInfo, password: str = ""):
    linux_user_obj = LinuxUser(user_info.name_eng)

    if not linux_user_obj.is_exist():
        print(f"User {user_info.name_eng} already exist")

        if not linux_user_obj.create(password=password):
            print(f"Create user {user_info.name_eng} failed")
            return

    linux_user_obj.uid = user_info.linux_user.uid
    linux_user_obj.gid = user_info.linux_user.gid


def create_linux_users(user_info_list: List[UserInfo], password: str = ""):
    for user_info in user_info_list:
        create_user(user_info=user_info, password=password)
