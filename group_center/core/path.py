import os
import sys
from typing import Optional


def get_tmpfs_path() -> str:
    if sys.platform == "linux":
        return "/dev/shm"

    return ""


def get_rt_str_path(pid: Optional[int]) -> str:
    if pid is None:
        pid = os.getpid()
    tmp_dir_path = get_tmpfs_path()
    file_path = os.path.join(tmp_dir_path, f"nvi_notify_{pid}_rt_str.txt")

    return file_path
