import os
import tempfile
import platform
from typing import Optional, Dict, Any
from pathlib import Path
from functools import lru_cache
import threading
import time


class EnvCache:
    """环境变量缓存类"""

    _instance = None
    _lock = threading.Lock()
    _cache: Dict[str, Any] = {}
    _last_update: float = 0.0
    _update_interval: float = 60.0  # 60秒更新间隔

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """获取缓存值

        Args:
            key: 缓存键
            default: 默认值

        Returns:
            缓存值或默认值
        """
        with cls._lock:
            if time.time() - cls._last_update > cls._update_interval:
                cls._cache = dict(os.environ)
                cls._last_update = time.time()
            return cls._cache.get(key, default)


@lru_cache(maxsize=128)
def get_env_string(key: str, default_value: str = "") -> str:
    """获取环境变量字符串值

    Args:
        key: 环境变量键
        default_value: 默认值

    Returns:
        str: 环境变量值或默认值
    """
    value = EnvCache().get(key, default_value)
    return str(value).strip()


@lru_cache(maxsize=128)
def get_env_int(key: str, default_value: int = 0) -> int:
    """获取环境变量整数值

    Args:
        key: 环境变量键
        default_value: 默认值

    Returns:
        int: 环境变量值或默认值

    Raises:
        ValueError: 如果值无法转换为整数
    """
    value = EnvCache().get(key)
    if value is None:
        return default_value
    try:
        return int(value)
    except ValueError as e:
        raise ValueError(f"Invalid integer value for environment variable {key}") from e


@lru_cache(maxsize=128)
def get_env_float(key: str, default_value: float = 0.0) -> float:
    """获取环境变量浮点数值

    Args:
        key: 环境变量键
        default_value: 默认值

    Returns:
        float: 环境变量值或默认值

    Raises:
        ValueError: 如果值无法转换为浮点数
    """
    value = EnvCache().get(key)
    if value is None:
        return default_value
    try:
        return float(value)
    except ValueError as e:
        raise ValueError(f"Invalid float value for environment variable {key}") from e


@lru_cache(maxsize=128)
def get_env_bool(key: str, default_value: bool = False) -> bool:
    """获取环境变量布尔值

    Args:
        key: 环境变量键
        default_value: 默认值

    Returns:
        bool: 环境变量值或默认值
    """
    value = EnvCache().get(key)
    if value is None:
        return default_value
    return str(value).lower() in ("true", "1", "yes", "y", "t")


def get_required_env(key: str) -> str:
    """获取必需的环境变量

    Args:
        key: 环境变量键

    Returns:
        str: 环境变量值

    Raises:
        ValueError: 如果环境变量未设置
    """
    value = EnvCache().get(key)
    if value is None:
        raise ValueError(f"Required environment variable {key} is not set")
    return str(value).strip()


@lru_cache(maxsize=1)
def get_user_home_dir() -> Path:
    """获取用户主目录路径

    Returns:
        Path: 用户主目录路径对象
    """
    return Path(os.path.expanduser("~"))


@lru_cache(maxsize=1)
def get_base_tmp_dir() -> Path:
    """获取系统临时目录路径

    Returns:
        Path: 系统临时目录路径对象
    """
    return Path(tempfile.gettempdir())


def get_a_tmp_dir(prefix: Optional[str] = None) -> Path:
    """创建一个临时目录

    Args:
        prefix: 目录名前缀

    Returns:
        Path: 创建的临时目录路径对象
    """
    dir_path = Path(tempfile.mkdtemp(prefix=prefix))
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


if __name__ == "__main__":
    try:
        print(f"User home: {get_user_home_dir()}")
        print(f"Base temp: {get_base_tmp_dir()}")
        print(f"New temp: {get_a_tmp_dir('group_center_')}")

        # 检测操作系统并获取CUDA信息
        if platform.system() == "Linux":
            cuda_home = get_env_string("CUDA_HOME")
            if cuda_home:
                print(f"\nLinux系统检测到CUDA_HOME: {cuda_home}")
            else:
                print("\nLinux系统未检测到CUDA_HOME环境变量")
    except Exception as e:
        print(f"Error: {e}")
