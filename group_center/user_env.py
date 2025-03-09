import os
import re
import sys
import subprocess
from typing import List, Optional

from group_center.core.path import get_rt_str_path


def get_python_version() -> str:
    """获取Python版本字符串"""
    version_str = sys.version.split()[0].strip()
    return version_str


PythonVersion = get_python_version()


def ENV_SCREEN_NAME_FULL() -> str:
    return os.getenv("STY", "").strip()


def _parse_screen_name() -> tuple[str, str]:
    full_name = ENV_SCREEN_NAME_FULL()
    parts = full_name.split(".") if full_name else []
    if len(parts) < 2:
        return ("", "")
    return (parts[0], ".".join(parts[1:]).strip())


def ENV_SCREEN_SESSION_ID() -> str:
    return _parse_screen_name()[0]


def ENV_SCREEN_SESSION_NAME() -> str:
    return _parse_screen_name()[1]


def is_in_screen_session() -> bool:
    return ENV_SCREEN_SESSION_NAME() != ""


def ENV_CUDA_ROOT() -> str:
    cuda_home: str = os.getenv("CUDA_HOME", "").strip()
    nvcc_path: str = os.path.join(cuda_home, "bin", "nvcc")

    cuda_nvcc_bin: str = ""

    if os.path.exists(nvcc_path):
        cuda_nvcc_bin = nvcc_path
    else:
        cuda_toolkit_root = os.getenv("CUDAToolkit_ROOT", "").strip()
        nvcc_path = os.path.join(cuda_toolkit_root, "bin", "nvcc")
        if os.path.exists(nvcc_path):
            cuda_nvcc_bin = nvcc_path

    return cuda_nvcc_bin


def CUDA_VERSION(nvcc_path: str = "") -> str:
    nvcc_path = nvcc_path.strip()
    if not nvcc_path or not os.path.exists(nvcc_path):
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
    return os.getenv("LOCAL_RANK", "").strip()


def ENV_CUDA_WORLD_SIZE() -> str:
    return os.getenv("LOCAL_WORLD_SIZE", "").strip()


def cuda_local_rank() -> int:
    local_rank = ENV_CUDA_LOCAL_RANK().strip()
    if local_rank == "":
        return -1
    try:
        return int(local_rank)
    except Exception:
        return -1


def cuda_world_size() -> int:
    world_size = ENV_CUDA_WORLD_SIZE().strip()
    if world_size == "":
        return -1
    try:
        return int(world_size)
    except Exception:
        return -1


def is_first_card_process() -> bool:
    if cuda_world_size() < 2:
        return True

    return cuda_local_rank() == 0


def RUN_COMMAND() -> str:
    return " ".join(sys.argv).strip()


def CONDA_ENV_NAME() -> str:
    run_command = RUN_COMMAND()

    pattern = r"envs/(.*?)/bin/python "
    match = re.search(pattern, run_command)
    if match:
        conda_env_name = match.group(1)
        env_str = conda_env_name
    else:
        env_str = os.getenv("CONDA_DEFAULT_ENV", "")

    env_str = env_str.strip()

    if env_str == "":
        env_str = "base"

    return env_str


def set_realtime_str(rt_str: str, pid: Optional[int] = None) -> bool:
    """设置实时字符串到临时文件

    Args:
        rt_str: 要写入的字符串内容
        pid: 进程ID，如果为None则使用当前进程ID

    Returns:
        bool: 是否成功写入
    """
    try:
        file_path = get_rt_str_path(pid=pid)
        if not os.path.exists(file_path):
            return False

        # Format the string
        rt_str = rt_str.strip()

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(rt_str)
        return True
    except Exception:
        return False


def show_realtime_str(pid: Optional[int] = None) -> str:
    """从临时文件读取实时字符串

    Args:
        pid: 进程ID，如果为None则使用当前进程ID

    Returns:
        str: 读取到的字符串内容，如果失败返回空字符串
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

    # 基本信息表
    table = Table(title="环境信息概览", box=box.ROUNDED)
    table.add_column("类别", justify="left", style="cyan")
    table.add_column("值", justify="left", style="green")

    table.add_row("Python 版本", PythonVersion)
    table.add_row("Conda 环境", CONDA_ENV_NAME())
    table.add_row("CUDA 版本", CUDA_VERSION() or "未找到")
    table.add_row("Screen 会话", ENV_SCREEN_SESSION_NAME() or "无")

    console.print(table)

    # 详细环境信息
    console.print("\n[bold]详细环境信息:[/bold]")
    console.print(f"[cyan]Screen 全名:[/cyan] {ENV_SCREEN_NAME_FULL()}")
    console.print(f"[cyan]Screen ID:[/cyan] {ENV_SCREEN_SESSION_ID()}")
    console.print(f"[cyan]CUDA 根目录:[/cyan] {ENV_CUDA_ROOT() or '未找到'}")
    console.print(f"[cyan]CUDA 本地 Rank:[/cyan] {ENV_CUDA_LOCAL_RANK() or '未设置'}")
    console.print(f"[cyan]CUDA World Size:[/cyan] {ENV_CUDA_WORLD_SIZE() or '未设置'}")
    console.print(f"[cyan]运行命令:[/cyan] {RUN_COMMAND()}")
