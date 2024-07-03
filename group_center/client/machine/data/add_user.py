from typing import List

from group_center.client.user.datatype.user_info import UserInfo


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


def linux_add_user_list(user_info_list: List[UserInfo], password: str = ""):
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

    return final_text
