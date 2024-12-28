import os

from config import global_config

__version__ = "1.8.2"


def get_version_path() -> str:
    return os.path.join(global_config.path_dir_config, "version.txt")


def get_version(version_path) -> str:
    if not os.path.exists(version_path):
        return ""

    with open(version_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    version_list = content.split(".")

    if len(version_list) != 3:
        return ""

    for i in version_list:
        if not i.isdigit():
            return ""

    return content


if __name__ == "__main__":
    print(__version__)
