from typing import Tuple

from group_center.utils.envs import *


def get_env_machine_config() -> Tuple[str, str, str, str]:
    url = get_env_string("GROUP_CENTER_URL")

    machine_name_full = \
        get_env_string("GROUP_CENTER_MACHINE_NAME")

    machine_name_short = \
        get_env_string("SERVER_NAME_SHORT")
    if machine_name_short == "":
        machine_name_short = get_env_string("GROUP_CENTER_MACHINE_NAME_SHORT")

    machine_password = \
        get_env_string("GROUP_CENTER_PASSWORD")
    if machine_password == "":
        machine_password = get_env_string("GROUP_CENTER_MACHINE_PASSWORD")

    return url,machine_name_full ,machine_name_short, machine_password


if __name__ == "__main__":
    print(get_env_machine_config())
