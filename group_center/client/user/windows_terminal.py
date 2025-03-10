import glob
import os
import platform
import argparse
import uuid
import json
from typing import List

from group_center.utils.log.logger import set_print_mode

set_print_mode(True)

from group_center.core.group_center_machine import (
    set_group_center_host_url,
    set_machine_name_short,
    set_machine_password,
    group_center_login,
)
from group_center.core.feature.remote_config import get_machine_config_json_str

from group_center.utils.log.logger import get_logger

LOGGER = get_logger()


def get_options() -> argparse.Namespace:
    """获取命令行参数 / Get command line arguments

    Returns:
        argparse.Namespace: 包含解析后参数的命名空间 / Namespace containing parsed arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--host",
        type=str,
        default="",
        help="Group Center 主机地址 / Group Center host URL",
    )
    parser.add_argument(
        "--center-name",
        type=str,
        default="",
        help="Group Center 名称 / Group Center name",
    )
    parser.add_argument(
        "--center-password",
        type=str,
        default="",
        help="Group Center 密码 / Group Center password",
    )
    parser.add_argument("--user-name", type=str, default="", help="用户名 / User name")

    opt = parser.parse_args()

    return opt


def connect_to_group_center(opt: argparse.Namespace):
    """连接到 Group Center / Connect to Group Center

    Args:
        opt (argparse.Namespace): 包含连接参数的命名空间 / Namespace containing connection parameters
    """
    set_group_center_host_url(opt.host)
    set_machine_name_short(opt.center_name)
    set_machine_password(opt.center_password)

    group_center_login()


def get_windows_terminal_config_path() -> str:
    """获取 Windows 终端配置文件路径 / Get Windows Terminal config file path

    Returns:
        str: 配置文件路径 / Config file path
    """
    # 检查是否是 Windows 系统 / Check if system is Windows
    if platform.system() != "Windows":
        return ""

    current_user_dir = os.path.expanduser("~")

    root_dir = os.path.join(current_user_dir, "AppData", "Local", "Packages")

    pattern = os.path.join(root_dir, "Microsoft.WindowsTerminal*")

    matched_paths = glob.glob(pattern)

    for path in matched_paths:
        settings_json = os.path.join(path, "LocalState", "settings.json")
        if os.path.exists(settings_json):
            return settings_json.strip()
        else:
            return ""

    return ""


def main():
    """主函数，添加 SSH 配置到 Windows 终端 / Main function to add SSH config to Windows Terminal"""
    LOGGER.info("Windows Terminal 添加 SSH / Windows Terminal add SSH")

    opt = get_options()

    connect_to_group_center(opt)

    # JSON 文件路径 / JSON file path
    json_path = get_windows_terminal_config_path()
    LOGGER.info("Windows Terminal 配置文件路径: " + json_path)
    if len(json_path) == 0:
        LOGGER.error(
            "Windows Terminal 配置文件路径为空 / Windows Terminal config path is empty"
        )
        exit(1)
    if not os.path.exists(json_path):
        LOGGER.error(
            "Windows Terminal 配置文件不存在 / Windows Terminal config file does not exist"
        )
        exit(1)

    json_dict: dict = json.load(open(json_path, "r"))
    if not (
        "profiles" in json_dict.keys()
        and "list" in json_dict["profiles"].keys()
        and isinstance(json_dict["profiles"]["list"], list)
    ):
        LOGGER.error("无效的 JSON 文件 / Invalid JSON file")
        exit(1)

    user_name = str(opt.user_name).strip()

    if len(user_name) == 0:
        LOGGER.error("无效的用户名 / Invalid user name")
        exit(1)

    machine_list_json = get_machine_config_json_str()
    machine_list: List[dict] = json.loads(machine_list_json)

    config_list: List[dict] = json_dict["profiles"]["list"]

    count = 0
    for machine_dict in machine_list:
        host = machine_dict["host"]
        name_eng = machine_dict["nameEng"]

        command_line = f"ssh {user_name}@{host}"

        # 忽略已存在的配置 / Ignore existing config
        found = False
        for config in config_list:
            if (
                "commandline" in config.keys()
                and config["commandline"].strip() == command_line
            ):
                LOGGER.info(
                    f"跳过 {name_eng}-{user_name}，因为已存在 / Skip {name_eng}-{user_name} because exists"
                )
                found = True
                break
        if found:
            continue

        config_list.append(
            {
                "commandline": command_line,
                "guid": "{" + str(uuid.uuid4()) + "}",
                "hidden": False,
                "name": f"{name_eng}-{user_name}",
            }
        )
        count += 1

    LOGGER.info(f"添加了 {count} 个 SSH 配置 / Added {count} SSH configs")

    json_dict["profiles"]["list"] = config_list

    with open(json_path, "w") as f:
        json.dump(json_dict, f, indent=4)

    LOGGER.success("成功! / Success!")


if __name__ == "__main__":
    main()
