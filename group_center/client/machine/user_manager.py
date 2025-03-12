import argparse
from typing import List
import json

from group_center.client.machine.feature.add_user import (
    linux_add_user_txt,
    create_linux_users,
    remove_linux_users,
    add_users_to_linux_group,
)
from group_center.client.user.datatype.user_info import get_user_info_list, UserInfo
from group_center.core.feature.remote_config import (
    get_user_config_json_str,
)
from group_center.core.group_center_machine import (
    set_group_center_host_url,
    set_machine_name_short,
    set_machine_password,
    group_center_login,
)


def get_options() -> argparse.Namespace:
    """
    获取命令行选项 / Get command line options

    Returns:
        argparse.Namespace: 解析后的选项对象 / Parsed options object containing command line arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", type=str, default="")
    parser.add_argument("--center-name", type=str, default="")
    parser.add_argument("--center-password", type=str, default="")

    parser.add_argument(
        "--add-user-txt",
        type=str,
        default=None,
        nargs="?",
        const="add_user.txt",
        help="保存用户添加命令到文本文件 / Save user addition commands to a text file",
    )
    parser.add_argument("--user-password", type=str, default="")
    parser.add_argument(
        "--user-password-file",
        type=str,
        help="从文件中读取密码，避免特殊字符问题 / Read password from file to avoid special character issues",
    )

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

    # 如果指定了密码文件，则从文件中读取密码
    if opt.user_password_file:
        try:
            with open(opt.user_password_file, "r") as f:
                opt.user_password = f.read().strip()
        except Exception as e:
            print(f"无法从文件读取密码: {e}")

    return opt


def connect_to_group_center(opt: argparse.Namespace) -> None:
    """
    连接到Group Center服务 / Connect to the Group Center service

    Args:
        opt (argparse.Namespace): 包含连接详细信息的命令行选项 / Command line options containing connection details
    """
    set_group_center_host_url(opt.host)
    set_machine_name_short(opt.center_name)
    set_machine_password(opt.center_password)

    group_center_login()


def create_user(opt: argparse.Namespace, user_info_list: List[UserInfo]) -> None:
    """
    在系统上创建新用户账户 / Create new user accounts on the system

    Args:
        opt (argparse.Namespace): 包含创建参数的命令行选项 / Command line options containing creation parameters
        user_info_list (List[UserInfo]): 要处理的用户信息对象列表 / List of user information objects to process
    """
    password: str = opt.user_password

    create_linux_users(user_info_list, password)


def save_add_user_text(opt: argparse.Namespace, user_info_list: List[UserInfo]) -> None:
    """
    将用户添加说明保存到文本文件 / Save user addition instructions to a text file

    Args:
        opt (argparse.Namespace): 包含输出路径和密码详细信息的选项 / Options including output path and password details
        user_info_list (List[UserInfo]): 要记录的用户信息对象 / User information objects to document
    """
    save_path: str = opt.add_user_txt
    password: str = opt.user_password

    linux_add_user_text = linux_add_user_txt(
        user_info_list=user_info_list, password=password
    )

    with open(save_path, "w") as f:
        f.write(linux_add_user_text)

    print("Add user text saved to:", save_path)
    print(f"Please run 'newusers {save_path}' to add users.")


def main() -> None:
    """
    用户管理模块的主执行入口 / Main execution entry point for the user management module
    """
    opt = get_options()

    connect_to_group_center(opt)

    have_option: bool = False

    # Get User List
    user_config_json = get_user_config_json_str()
    user_dict_list = json.loads(user_config_json)
    user_info_list: List[UserInfo] = get_user_info_list(user_dict_list)

    print(f"Total User Count: {len(user_info_list)}")

    if opt.year > 0:
        user_info_list = [
            user_info for user_info in user_info_list if user_info.year == opt.year
        ]

    if opt.create_users:
        have_option = True
        create_user(opt, user_info_list)

    if opt.remove_users:
        have_option = True
        remove_linux_users(user_info_list)

    if opt.add_user_txt is not None:
        have_option = True
        save_add_user_text(opt, user_info_list)

    if opt.user_group and isinstance(opt.user_group, str):
        have_option = True
        linux_groups = opt.user_group
        linux_groups_list = linux_groups.split(",")

        for linux_group in linux_groups_list:
            add_users_to_linux_group(user_info_list, linux_group)

    if not have_option:
        print("No option!")
    else:
        print("Done!")


if __name__ == "__main__":
    main()
