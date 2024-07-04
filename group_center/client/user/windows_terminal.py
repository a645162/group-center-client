import glob
import os
import platform
import argparse
import uuid
from typing import List

from group_center.utils.log.logger import set_is_print_mode

set_is_print_mode(True)

from group_center.core.group_center_machine import *
from group_center.core.feature.remote_config import get_machine_config_json_str

logger = get_logger()


def get_options():
    parser = argparse.ArgumentParser()

    parser.add_argument("--host", type=str, default="")
    parser.add_argument("--center-name", type=str, default="")
    parser.add_argument("--center-password", type=str, default="")

    parser.add_argument("--user-name", type=str, default="")

    opt = parser.parse_args()

    return opt


def connect_to_group_center(opt):
    set_group_center_host_url(opt.host)
    set_machine_name_short(opt.center_name)
    set_machine_password(opt.center_password)

    group_center_login()


def get_windows_terminal_config_path():
    # Check is Windows
    if platform.system() != 'Windows':
        return ""

    current_user_dir = os.path.expanduser('~')

    root_dir = os.path.join(current_user_dir, 'AppData', 'Local', 'Packages')

    pattern = os.path.join(root_dir, "Microsoft.WindowsTerminal*")

    matched_paths = glob.glob(pattern)

    for path in matched_paths:
        settings_json = os.path.join(path, 'LocalState', 'settings.json')
        if os.path.exists(settings_json):
            return settings_json.strip()
        else:
            return ""


def main():
    logger.info("Windows Terminal add SSH")

    opt = get_options()

    connect_to_group_center(opt)

    json_path = get_windows_terminal_config_path()
    logger.info("Windows Terminal Config Path:")
    logger.info(json_path)
    json_dict: dict = json.load(open(json_path, 'r'))
    if not (
            "profiles" in json_dict.keys() and
            "list" in json_dict["profiles"].keys() and
            isinstance(json_dict["profiles"]["list"], list)
    ):
        logger.error("Invalid json")
        exit(1)

    user_name = str(opt.user_name).strip()

    if len(user_name) == 0:
        logger.error("Invalid user name")
        exit(1)

    machine_list_json = get_machine_config_json_str()
    machine_list: List[dict] = json.loads(machine_list_json)

    config_list: List[dict] = json_dict["profiles"]["list"]

    count = 0
    for machine_dict in machine_list:
        host = machine_dict["host"]
        name_eng = machine_dict["nameEng"]

        command_line = f"ssh {user_name}@{host}"

        # Ignore Exists
        found = False
        for config in config_list:
            if (
                    "commandline" in config.keys() and
                    config["commandline"].strip() == command_line
            ):
                logger.info(f"Skip {name_eng}-{user_name} because exists")
                found = True
                break
        if found:
            continue

        config_list.append({
            "commandline": command_line,
            "guid": "{" + str(uuid.uuid4()) + "}",
            "hidden": False,
            "name": f"{name_eng}-{user_name}"
        })
        count += 1

    logger.info(f"Add {count} SSH Config")

    json_dict["profiles"]["list"] = config_list

    with open(json_path, 'w') as f:
        json.dump(json_dict, f, indent=4)

    logger.success("Success!")


if __name__ == "__main__":
    main()
