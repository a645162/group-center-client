import os
import platform


def is_run_on_linux():
    return platform.system() == "Linux"


def is_run_with_sudo() -> bool:
    return os.geteuid() == 0
