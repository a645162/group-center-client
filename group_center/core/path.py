import os  # 操作系统接口 / OS interface
import sys  # 系统相关参数和函数 / System-specific parameters and functions
from typing import Optional, Union, Type
from pathlib import Path  # 面向对象的路径操作 / Object-oriented path manipulation
from functools import lru_cache  # 缓存装饰器 / Cache decorator


class PathUtils:
    """路径工具类
    Path utility class
    """

    _instance: Optional[Type["PathUtils"]] = None  # 单例实例 / Singleton instance

    def __new__(cls) -> "PathUtils":
        """单例模式实现
        Singleton pattern implementation
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @staticmethod
    @lru_cache(maxsize=1)
    def get_tmpfs_path() -> Optional[Path]:
        """获取临时文件系统路径
        Get temporary filesystem path

        Returns:
            Optional[Path]: 在Linux系统返回/dev/shm，其他系统返回空
            Returns /dev/shm on Linux, None on other systems
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
        Get real-time string file path

        Args:
            pid (Optional[int]): 进程ID，如果为None则使用当前进程ID
            Process ID, uses current process ID if None

        Returns:
            Path: 实时字符串文件路径对象
            Real-time string file path object
        """
        if pid is None:
            pid = os.getpid()
        tmpfs_path: Optional[Path] = PathUtils.get_tmpfs_path()
        if tmpfs_path is None:
            raise RuntimeError("Temporary filesystem path not available")
        return tmpfs_path / f"nvi_notify_{pid}_rt_str.txt"

    @staticmethod
    def ensure_dir_exists(path: Union[str, Path]) -> Path:
        """确保目录存在
        Ensure directory exists

        Args:
            path (Union[str, Path]): 目录路径
            Directory path

        Returns:
            Path: 确保存在的目录路径对象
            Directory path object that is ensured to exist
        """
        path_obj: Path = Path(path)
        path_obj.mkdir(parents=True, exist_ok=True)
        return path_obj

    @staticmethod
    def is_subpath(child: Union[str, Path], parent: Union[str, Path]) -> bool:
        """检查路径是否为子路径
        Check if path is a subpath

        Args:
            child (Union[str, Path]): 子路径
            Child path
            parent (Union[str, Path]): 父路径
            Parent path

        Returns:
            bool: 如果是子路径返回True
            True if child is a subpath of parent
        """
        try:
            child_path: Path = Path(child).resolve()
            parent_path: Path = Path(parent).resolve()
            return parent_path in child_path.parents
        except Exception:
            return False

    @staticmethod
    def get_relative_path(path: Union[str, Path], start: Union[str, Path]) -> Path:
        """获取相对路径
        Get relative path

        Args:
            path (Union[str, Path]): 目标路径
            Target path
            start (Union[str, Path]): 起始路径
            Starting path

        Returns:
            Path: 相对路径对象
            Relative path object
        """
        return Path(path).resolve().relative_to(Path(start).resolve())


def get_tmpfs_path() -> Path:
    """获取临时文件系统路径
    Get temporary filesystem path

    Returns:
        Path: 在Linux系统返回/dev/shm，其他系统返回系统临时目录
        Returns /dev/shm on Linux, system temp directory on other systems
    """
    tmpfs_path: Optional[Path] = PathUtils.get_tmpfs_path()
    if tmpfs_path is None:
        return Path(os.getenv("TEMP", "/tmp"))
    return tmpfs_path


def get_rt_str_path(pid: Optional[int] = None) -> Path:
    """获取实时字符串文件路径
    Get real-time string file path

        Args:
            pid (Optional[int]): 进程ID，如果为None则使用当前进程ID
            Process ID, uses current process ID if None

        Returns:
        Path: 实时字符串文件路径对象
        Real-time string file path object
    """
    return PathUtils.get_rt_str_path(pid)


def cleanup_unused_rt_files():
    """清理未使用的实时字符串文件
    Clean up unused real-time string files
    """

    # Check is Linux
    if sys.platform != "linux":
        return

    tmpfs_path: Optional[Path] = PathUtils.get_tmpfs_path()
    if tmpfs_path is None:
        return

    for file in tmpfs_path.glob("nvi_notify_*_rt_str.txt"):
        if not file.exists():
            continue

        file_name = file.name
        import re

        pid = re.findall(r"nvi_notify_(\d+)_rt_str.txt", file_name)[0]
        if pid.isdigit():
            pid = int(pid)
        else:
            continue

        try:
            if not os.path.exists(f"/proc/{pid}"):
                os.remove(file)
        except Exception as e:
            print(f"Failed to remove file {file}: {e}")
            continue


if __name__ == "__main__":
    cleanup_unused_rt_files()
