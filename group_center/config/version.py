import os
from typing import List

try:
    from typing import Final
except ImportError:
    from typing_extensions import Final

from group_center.config import global_config

# 当前版本号 / Current version number
__version__: Final[str] = "2.6.1"


def get_version_path() -> str:
    """获取版本文件路径
    Get version file path

    Returns:
        str: 版本文件路径 | Version file path
    """
    return os.path.join(global_config.path_dir_config, "version.txt")


def get_version(version_path: str) -> str:
    """从版本文件中获取版本号
    Get version number from version file

    Args:
        version_path (str): 版本文件路径 | Version file path

    Returns:
        str: 版本号 | Version number
    """
    if not os.path.exists(version_path):
        return ""

    with open(version_path, "r", encoding="utf-8") as f:
        content: str = f.read().strip()

    version_list: List[str] = content.split(".")

    if len(version_list) != 3:
        return ""

    for i in version_list:
        if not i.isdigit():
            return ""

    return content


if __name__ == "__main__":
    print(__version__)
