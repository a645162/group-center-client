import sys


def get_tmpfs_path() -> str:
    if sys.platform == "linux":
        return "/dev/shm"

    return ""
