import os

from config import global_config


def get_version() -> str:
    version_path = \
        os.path.join(global_config.path_dir_config, "version.txt")

    with open(version_path, "r") as f:
        version_text = f.read().strip()

    return version_text


if __name__ == "__main__":
    print(get_version())
