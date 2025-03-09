import os
import re
import sys
import subprocess
from typing import Optional, Union

from group_center.core.path import get_rt_str_path


def get_python_version() -> str:
    """获取Python版本字符串 (Get Python version string)

    Returns:
        str: Python版本字符串 (Python version string)
    """
    version_str = sys.version.split()[0].strip()
    return version_str


PythonVersion = get_python_version()


def ENV_SCREEN_NAME_FULL() -> str:
    """获取Screen会话全名 (Get full Screen session name)

    Returns:
        str: Screen会话全名 (Full Screen session name)
    """
    return os.getenv("STY", "").strip()


def _parse_screen_name() -> tuple[str, str]:
    """解析Screen会话名称 (Parse Screen session name)

    Returns:
        tuple[str, str]: (会话ID, 会话名称) (Session ID, Session name)
    """
    full_name = ENV_SCREEN_NAME_FULL()
    parts = full_name.split(".") if full_name else []
    if len(parts) < 2:
        return ("", "")
    return (parts[0], ".".join(parts[1:]).strip())


def ENV_SCREEN_SESSION_ID() -> str:
    """获取Screen会话ID (Get Screen session ID)

    Returns:
        str: 屏幕会话ID (Screen session ID)
    """
    return _parse_screen_name()[0]


def ENV_SCREEN_SESSION_NAME() -> str:
    """获取Screen会话名称 (Get Screen session name)

    Returns:
        str: 屏幕会话名称 (Screen session name)
    """
    return _parse_screen_name()[1]


def is_in_screen_session() -> bool:
    """检查是否在Screen会话中 (Check if in Screen session)

    Returns:
        bool: 是否在Screen会话中 (是否在Screen会话中)
    """
    return ENV_SCREEN_SESSION_NAME() != ""


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


def RUN_COMMAND() -> str:
    """获取当前运行命令 (Get current run command)

    Returns:
        str: 当前执行的命令字符串
    """
    return " ".join(sys.argv).strip()


def CONDA_ENV_NAME() -> str:
    """获取当前Conda环境名称 (Get current Conda environment name)

    Returns:
        str: Conda环境名称 (Conda environment name)
    """
    run_command = RUN_COMMAND()
    pattern = r"envs/(.*?)/bin/python "
    match = re.search(pattern, run_command)
    if match:
        conda_env_name = match.group(1)
        env_str = conda_env_name
    else:
        env_str = os.getenv("CONDA_DEFAULT_ENV", "")

    env_str = env_str.strip() or "base"
    return env_str


def set_realtime_str(rt_str: str, pid: Optional[int] = None) -> bool:
    """设置实时字符串到临时文件 (Write real-time string to temp file)

    Args:
        rt_str (str): 要写入的字符串内容
        pid (int, optional): 目标进程ID (Target process ID)

    Returns:
        bool: 写入是否成功
    """
    try:
        file_path = get_rt_str_path(pid=pid)
        if not os.path.exists(file_path):
            return False

        rt_str = rt_str.strip()
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(rt_str)
        return True
    except Exception:
        return False


def show_realtime_str(pid: Optional[int] = None) -> str:
    """从临时文件读取实时字符串 (Read real-time string from temp file)

    Args:
        pid (int, optional): 目标进程ID (Target process ID)

    Returns:
        str: 读取到的字符串内容 (Empty if failed)
    """
    try:
        file_path = get_rt_str_path(pid=pid)
        if not os.path.exists(file_path):
            return ""

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        return content
    except Exception:
        return ""


if __name__ == "__main__":
    from rich.console import Console
    from rich.table import Table
    from rich import box

    console = Console()

    table = Table(title="环境信息概览", box=box.ROUNDED)
    table.add_column("类别", justify="left", style="cyan")
    table.add_column("值", justify="left", style="green")

    table.add_row("Python 版本", PythonVersion)
    table.add_row("Conda 环境", CONDA_ENV_NAME())
    table.add_row("CUDA 版本", CUDA_VERSION() or "未找到")
    table.add_row("Screen 会话", ENV_SCREEN_SESSION_NAME() or "无")

    console.print(table)

    console.print("\n[bold]详细环境信息:[/bold]")
    console.print(f"[cyan]Screen 全名:[/cyan] {ENV_SCREEN_NAME_FULL()}")
    console.print(f"[cyan]Screen ID:[/cyan] {ENV_SCREEN_SESSION_ID()}")
    console.print(f"[cyan]CUDA 根目录:[/cyan] {ENV_CUDA_ROOT() or '未找到'}")
    console.print(f"[cyan]CUDA 本地 Rank:[/cyan] {ENV_CUDA_LOCAL_RANK() or '未设置'}")
    console.print(f"[cyan]CUDA World Size:[/cyan] {ENV_CUDA_WORLD_SIZE() or '未设置'}")
    console.print(f"[cyan]运行命令:[/cyan] {RUN_COMMAND()}")
