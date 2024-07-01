import argparse

from group_center.client.machine.data.add_user import linux_add_user_list
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

    parser.add_argument(
        "-c",
        "--create-user",
        help="Create Users",
        action="store_true",
    )

    opt = parser.parse_args()

    return opt


def connect_to_group_center(opt):
    set_group_center_host_url(opt.host)
    set_machine_name_short(opt.center_name)
    set_machine_password(opt.center_password)

    group_center_login()


def create_user():
    user_config_json = get_user_config_json_str()
    user_list = json.loads(user_config_json)

    linux_add_user_text = linux_add_user_list(user_list)

    print(linux_add_user_text)


def save_add_user_text(opt):
    save_path: str = opt.add_user_txt
    password: str = opt.user_password

    if not save_path:
        save_path = "add_user.txt"

    user_config_json = get_user_config_json_str()
    user_list = json.loads(user_config_json)

    linux_add_user_text = linux_add_user_list(
        user_list=user_list,
        password=password
    )

    with open(save_path, "w") as f:
        f.write(linux_add_user_text)


def main():
    opt = get_options()

    connect_to_group_center(opt)

    if opt.create_user:
        create_user()

    if opt.add_user:
        save_add_user_text(opt)


if __name__ == "__main__":
    main()
