import os
import platform


def is_run_on_linux() -> bool:
    return platform.system() == "Linux"


def is_run_with_sudo() -> bool:
    return os.geteuid() == 0


def get_os_release_id():
    for line in cat_info("/etc/os-release").strip().split("\n"):
        key, value = line.rstrip().split("=", 1)
        if key == "ID":
            return value.strip('"')
