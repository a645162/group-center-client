from typing import List


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


def linux_add_user_list(user_list: List[dict], password: str = ""):
    final_text = ""

    for user_dict in user_list:
        user_name: str = user_dict["nameEng"]

        uid: int = user_dict["linuxUser"]["uid"]
        gid: int = user_dict["linuxUser"]["gid"]

        group_name: str = user_name
        home_dir: str = f"/home/{user_name}"
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
