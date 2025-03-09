import os
import subprocess
from typing import Optional


def ENV_CUDA_ROOT() -> str:
    """获取CUDA根目录路径 (Get CUDA root directory path)

    Returns:
        str: CUDA根目录路径 (CUDA root directory path)
    """
    cuda_home = os.getenv("CUDA_HOME", "").strip()
    nvcc_path = os.path.join(cuda_home, "bin", "nvcc")

    cuda_nvcc_bin = ""
    if os.path.exists(nvcc_path):
        cuda_nvcc_bin = nvcc_path
    else:
        cuda_toolkit_root = os.getenv("CUDAToolkit_ROOT", "").strip()
        nvcc_path = os.path.join(cuda_toolkit_root, "bin", "nvcc")
        if os.path.exists(nvcc_path):
            cuda_nvcc_bin = nvcc_path
    return cuda_nvcc_bin


def CUDA_VERSION(nvcc_path: Optional[str] = None) -> str:
    """获取CUDA版本 (Get CUDA version)

    Args:
        nvcc_path (str, optional): 指定nvcc路径 (Custom nvcc path)

    Returns:
        str: CUDA版本字符串 (CUDA version string)
    """
    if nvcc_path is not None and not os.path.exists(nvcc_path.strip()):
        nvcc_path = ENV_CUDA_ROOT()
    if not nvcc_path:
        return ""

    try:
        result = subprocess.run(
            [nvcc_path, "--version"], capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""

    for line in result.splitlines():
        if "release" in line:
            version_part = line.split(",")[-1].strip().lower()
            return version_part.replace("v", "", 1)
    return ""


def ENV_CUDA_LOCAL_RANK() -> str:
    """获取CUDA本地Rank (Get CUDA local rank)

    Returns:
        str: CUDA本地Rank值 (CUDA local rank value)
    """
    return os.getenv("LOCAL_RANK", "").strip()


def ENV_CUDA_WORLD_SIZE() -> str:
    """获取CUDA世界大小 (Get CUDA world size)

    Returns:
        str: CUDA世界大小值 (CUDA world size value)
    """
    return os.getenv("LOCAL_WORLD_SIZE", "").strip()


def cuda_local_rank() -> int:
    """将CUDA本地Rank转换为整数 (Convert CUDA local rank to integer)

    Returns:
        int: 转换后的Rank值 (-1表示失败)
    """
    local_rank = ENV_CUDA_LOCAL_RANK().strip()
    if not local_rank:
        return -1
    try:
        return int(local_rank)
    except Exception:
        return -1


def cuda_world_size() -> int:
    """将CUDA世界大小转换为整数 (Convert CUDA world size to integer)

    Returns:
        int: 转换后的世界大小 (-1表示失败)
    """
    world_size = ENV_CUDA_WORLD_SIZE().strip()
    if not world_size:
        return -1
    try:
        return int(world_size)
    except Exception:
        return -1


def is_first_card_process() -> bool:
    """检查是否是主卡进程 (Check if first GPU process)

    Returns:
        bool: 是否是主卡进程
    """
    if cuda_world_size() < 2:
        return True
    return cuda_local_rank() == 0
