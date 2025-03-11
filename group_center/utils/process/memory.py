from typing import List
import psutil


def get_process_memory_usage(pid: int) -> float:
    """
    获取给定进程ID的内存占用（以MB为单位）
    Get memory usage of the given process ID (in MB).

    Args:
        pid (int): 进程ID / Process ID

    Returns:
        float: 内存占用量（MB） / Memory usage in MB
    """
    try:
        process = psutil.Process(pid)
        # 获取RSS内存（实际物理内存）并转换为MB / Get RSS memory (actual physical memory) and convert to MB
        memory_info = process.memory_info()
        return memory_info.rss / (1024 * 1024)
    except psutil.NoSuchProcess:
        return 0.0


def get_total_memory_usage(pid_list: List[int]) -> float:
    """
    获取进程ID列表的总内存占用（以MB为单位）
    Get total memory usage for a list of process IDs (in MB).

    Args:
        pid_list (List[int]): 进程ID列表 / List of process IDs

    Returns:
        float: 总内存占用量（MB） / Total memory usage in MB
    """
    total_memory = 0.0
    for pid in pid_list:
        total_memory += get_process_memory_usage(pid)
    return total_memory
