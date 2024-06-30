import argparse

from group_center.core.feature.remote_config import (
    get_user_config_json_str,
)
from group_center.core.group_center_machine import *


def get_options():
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", type=str, default="")
    parser.add_argument("--name", type=str, default="")
    parser.add_argument("--password", type=str, default="")
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
    set_machine_name_short(opt.name)
    set_machine_password(opt.password)

    group_center_login()


def create_user():
    user_config_json = get_user_config_json_str()
    user_list = json.loads(user_config_json)
    print()


def main():
    opt = get_options()

    connect_to_group_center(opt)

    if opt.create_user:
        create_user()


if __name__ == "__main__":
    main()
