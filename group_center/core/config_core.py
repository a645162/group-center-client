from typing import Tuple

from group_center.utils.envs import *


def get_env_machine_config() -> Tuple[str, str, str]:
    url = get_env_string("GROUP_CENTER_URL")

    machine_name = \
        get_env_string("SERVER_NAME_SHORT")
    if machine_name == "":
        machine_name = get_env_string("GROUP_CENTER_MACHINE_NAME")

    machine_password = \
        get_env_string("GROUP_CENTER_PASSWORD")
    if machine_password == "":
        machine_password = get_env_string("GROUP_CENTER_MACHINE_PASSWORD")

    return url, machine_name, machine_password


if __name__ == "__main__":
    print(get_env_machine_config())
