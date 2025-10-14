import os
from typing import List, Union
from group_center.utils.process.memory import (
    get_process_memory_usage,
    get_total_memory_usage,
)

import psutil


def get_parent_process_pid(pid: int) -> int:
    """
    获取给定进程ID的父进程ID
    Get the parent process ID of the given process ID.

    Args:
        pid (int): 进程ID / Process ID

    Returns:
        int: 父进程ID / Parent process ID
    """

    if pid == -1:
        # Current Process
        return os.getppid()

    process = psutil.Process(pid)
    return process.ppid()


def get_process_name(pid: int) -> str:
    """
    获取给定进程ID的进程名称
    Get the process name of the given process ID.

    Args:
        pid (int): 进程ID / Process ID

    Returns:
        str: 进程名称 / Process name
    """
    process = psutil.Process(pid)
    return process.name()


def get_process_name_list(pid_list: List[int]) -> List[str]:
    """
    获取进程ID列表对应的进程名称列表
    Get the process names for a list of process IDs.

    Args:
        pid_list (List[int]): 进程ID列表 / List of process IDs

    Returns:
        List[str]: 进程名称列表 / List of process names
    """
    return [get_process_name(pid) for pid in pid_list]


def get_chain_of_process(pid: int) -> List[int]:
    """
    获取给定进程ID的进程链
    Get the process chain for the given process ID.

    Args:
        pid (int): 起始进程ID / Starting process ID

    Returns:
        List[int]: 进程链列表，从子进程到父进程 / List of process IDs in chain, from child to parent
    """

    if pid <= 0:
        pid = os.getpid()

    chain = []
    while pid > 0:
        chain.append(pid)
        pid = get_parent_process_pid(pid)
    return chain


def check_is_python_process(pid: Union[int, str]) -> bool:
    """
    检查给定进程ID是否属于Python进程
    Check if the given process ID belongs to a Python process.

    Args:
        pid (Union[int, str]): 进程ID，可以是整数或字符串 / Process ID, can be integer or string

    Returns:
        bool: 如果是Python进程返回True，否则返回False / Returns True if it's a Python process, False otherwise
    """
    try:
        if isinstance(pid, str):
            pid = int(pid)
        process = psutil.Process(pid)
        exe_path = process.exe()
        exe_name = os.path.basename(exe_path)

        index = exe_name.find(".")
        if index > -1:
            exe_name = exe_name[:index]
        exe_name = exe_name.strip().lower()

        return exe_name == "python" or exe_name == "python3"
    except Exception:
        return False


def get_top_python_process_pid(pid: int) -> int:
    """
    获取当前进程链中最顶层的Python进程ID
    Get the topmost Python process ID in the current process chain.

    Args:
        pid (int): 起始进程ID / Starting process ID

    Returns:
        int: 最顶层的Python进程ID，如果找不到返回-1 / Topmost Python process ID, returns -1 if not found
    """
    pid_list = get_chain_of_process(pid)

    if len(pid_list) < 2:
        return -1

    # Remove Self
    pid_list = pid_list[1:]

    pid_list.reverse()

    for pid in pid_list:
        if check_is_python_process(pid):
            return pid

    return -1


def get_process_path(pid: int) -> str:
    """
    获取给定进程ID的进程路径
    Get the process path of the given process ID.
    Args:
        pid (int): 进程ID / Process ID
    Returns:
        str: 进程路径 / Process path
    """
    process = psutil.Process(pid)
    return process.exe()


def get_child_processes(pid: int, recursive: bool = True) -> List[int]:
    """
    递归获取给定进程ID的所有子进程ID
    Recursively get all child process IDs for a given process ID.

    Args:
        pid (int): 父进程ID / Parent process ID
        recursive (bool): 是否递归获取子进程的子进程 / Whether to recursively get children of children

    Returns:
        List[int]: 子进程ID列表 / List of child process IDs
    """
    try:
        parent = psutil.Process(pid)
        children = parent.children(recursive=recursive)
        return [child.pid for child in children]
    except psutil.NoSuchProcess:
        return []


def kill_process_list(pid_list: List[int]) -> bool:
    """
    批量杀死进程
    Kill a list of processes by PID.

    Args:
        pid_list (List[int]): 进程ID列表 / List of process IDs
    """
    success = True

    for pid in pid_list:
        try:
            p = psutil.Process(pid)
            p.kill()
        except Exception as e:
            # 可根据需要打印或记录错误
            print(f"Error killing process {pid}: {e}")
            success = False

    return success


if __name__ == "__main__":
    print(get_parent_process_pid(-1))
    print(get_process_name(get_parent_process_pid(-1)))

    pid_list = get_chain_of_process(-1)
    print(pid_list)

    path_list = [get_process_path(pid) for pid in pid_list]
    print(path_list)

    p_name_list = get_process_name_list(pid_list)
    print(p_name_list)

    p_is_python_list = [check_is_python_process(pid) for pid in pid_list]
    print(p_is_python_list)

    print(get_top_python_process_pid(-1))

    current_pid = os.getpid()
    print(f"子进程列表: {get_child_processes(current_pid)}")
    print(f"当前进程内存占用: {get_process_memory_usage(current_pid):.2f} MB")

    print(f"进程链总内存占用: {get_total_memory_usage(pid_list):.2f} MB")
