import argparse
from typing import List

from group_center.client.machine.feature.add_user import (
    linux_add_user_txt,
    create_linux_users, remove_linux_users,
    add_users_to_linux_group,
)
from group_center.client.user.datatype.user_info import get_user_info_list, UserInfo
from group_center.core.feature.remote_config import (
    get_user_config_json_str,
)
from group_center.core.group_center_machine import *


def get_options():
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", type=str, default="")
    parser.add_argument("--center-name", type=str, default="")
    parser.add_argument("--center-password", type=str, default="")

    parser.add_argument("--add-user-txt", type=str, default="")
    parser.add_argument("--user-password", type=str, default="")

    parser.add_argument("--user-group", type=str, default="")

    parser.add_argument("--year", type=int, default=0)

    parser.add_argument(
        "-c",
        "--create-users",
        help="Create Users",
        action="store_true",
    )

    parser.add_argument(
        "-r",
        "--remove-users",
        help="Remove Users",
        action="store_true",
    )

    opt = parser.parse_args()

    return opt


def connect_to_group_center(opt):
    set_group_center_host_url(opt.host)
    set_machine_name_short(opt.center_name)
    set_machine_password(opt.center_password)

    group_center_login()


def create_user(opt, user_info_list: List[UserInfo]):
    password: str = opt.user_password

    create_linux_users(user_info_list, password)

# newusers add_user.txt
def save_add_user_text(opt, user_info_list: List[UserInfo]):
    save_path: str = opt.add_user_txt
    password: str = opt.user_password

    if not save_path:
        save_path = "add_user.txt"

    linux_add_user_text = linux_add_user_txt(
        user_info_list=user_info_list,
        password=password
    )

    with open(save_path, "w") as f:
        f.write(linux_add_user_text)


def main():
    opt = get_options()

    connect_to_group_center(opt)

    # Get User List
    user_config_json = get_user_config_json_str()
    user_dict_list = json.loads(user_config_json)
    user_info_list: List[UserInfo] = get_user_info_list(user_dict_list)

    if opt.year > 0:
        user_info_list = [
            user_info
            for user_info in user_info_list
            if user_info.year == opt.year
        ]

    if opt.create_users:
        create_user(opt, user_info_list)

    if opt.remove_users:
        remove_linux_users(user_info_list)

    if opt.add_user_txt:
        save_add_user_text(opt, user_info_list)

    if opt.user_group and isinstance(opt.user_group, str):
        linux_groups = opt.user_group
        linux_groups_list = linux_groups.split(",")

        for linux_group in linux_groups_list:
            add_users_to_linux_group(user_info_list, linux_group)


if __name__ == "__main__":
    main()
