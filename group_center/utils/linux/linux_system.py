import os
import platform
from typing import Optional

from group_center.utils.command.command import cat_info


def is_run_on_linux() -> bool:
    return platform.system() == "Linux"


def is_run_with_sudo() -> bool:
    """检查是否以sudo权限运行
    Check if running with sudo privileges

    Returns:
        bool: 如果以sudo权限运行返回True，否则返回False / Returns True if running with sudo, False otherwise
    """
    return os.geteuid() == 0


def get_os_release_id() -> Optional[str]:
    """获取Linux发行版ID
    Get Linux distribution ID

    Returns:
        Optional[str]: 返回发行版ID，如果未找到返回None / Returns distribution ID, or None if not found
    """
    for line in cat_info("/etc/os-release").strip().split("\n"):
        key, value = line.rstrip().split("=", 1)
        if key == "ID":
            return value.strip('"')
    return None
