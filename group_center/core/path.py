import os
import sys
from typing import Optional, Union
from pathlib import Path
from functools import lru_cache


class PathUtils:
    """路径工具类"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    @lru_cache(maxsize=1)
    def get_tmpfs_path() -> Optional[Path]:
        """获取临时文件系统路径

        Returns:
            Path: 在Linux系统返回/dev/shm，其他系统返回空
        """
        path: Optional[Path] = None

        if sys.platform == "linux":
            path = Path("/dev/shm")
            if not path.exists():
                path = None

        return path

    @staticmethod
    def get_rt_str_path(pid: Optional[int] = None) -> Path:
        """获取实时字符串文件路径

        Args:
            pid: 进程ID，如果为None则使用当前进程ID

        Returns:
            Path: 实时字符串文件路径对象
        """
        if pid is None:
            pid = os.getpid()
        return PathUtils.get_tmpfs_path() / f"nvi_notify_{pid}_rt_str.txt"

    @staticmethod
    def ensure_dir_exists(path: Union[str, Path]) -> Path:
        """确保目录存在

        Args:
            path: 目录路径

        Returns:
            Path: 确保存在的目录路径对象
        """
        path = Path(path)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def is_subpath(child: Union[str, Path], parent: Union[str, Path]) -> bool:
        """检查路径是否为子路径

        Args:
            child: 子路径
            parent: 父路径

        Returns:
            bool: 如果是子路径返回True
        """
        try:
            child = Path(child).resolve()
            parent = Path(parent).resolve()
            return parent in child.parents
        except Exception:
            return False

    @staticmethod
    def get_relative_path(path: Union[str, Path], start: Union[str, Path]) -> Path:
        """获取相对路径

        Args:
            path: 目标路径
            start: 起始路径

        Returns:
            Path: 相对路径对象
        """
        return Path(path).resolve().relative_to(Path(start).resolve())


def get_tmpfs_path() -> Path:
    """获取临时文件系统路径

    Returns:
        Path: 在Linux系统返回/dev/shm，其他系统返回系统临时目录
    """
    return PathUtils.get_tmpfs_path()


def get_rt_str_path(pid: Optional[int] = None) -> Path:
    """获取实时字符串文件路径

    Args:
        pid: 进程ID，如果为None则使用当前进程ID

    Returns:
        Path: 实时字符串文件路径对象
    """
    return PathUtils.get_rt_str_path(pid)


if __name__ == "__main__":
    print(get_tmpfs_path())
    print(get_rt_str_path())
