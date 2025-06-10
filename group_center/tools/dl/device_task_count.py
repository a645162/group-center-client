from nvitop import Device
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


def get_gpu_memory_info() -> List[Dict]:
    """
    获取所有GPU的显存信息

    Returns:
        List[Dict]: 包含每个GPU显存信息的列表
    """
    try:
        devices = Device.all()
        gpu_info = []

        for device in devices:
            memory_total = device.memory_total() / (1024**3)  # 转换为GiB
            memory_used = device.memory_used() / (1024**3)  # 转换为GiB
            memory_free = memory_total - memory_used

            info = {
                "gpu_id": device.index,
                "name": device.name(),
                "memory_total_gib": round(memory_total, 2),
                "memory_used_gib": round(memory_used, 2),
                "memory_free_gib": round(memory_free, 2),
                "memory_utilization": round((memory_used / memory_total) * 100, 2),
            }
            gpu_info.append(info)

        return gpu_info
    except Exception as e:
        logger.error(f"获取GPU信息失败: {e}")
        return []


def calculate_max_tasks_per_gpu(
    task_memory_gib: float, memory_buffer_gib: float = 0.5
) -> Dict:
    """
    计算每个GPU能支持的最大任务数

    Args:
        task_memory_gib (float): 单个任务需要的显存大小(GiB)
        memory_buffer_gib (float): 预留的缓冲显存(GiB)，默认0.5GiB

    Returns:
        Dict: 包含GPU信息和任务容量的字典
    """
    if task_memory_gib <= 0:
        raise ValueError("任务显存大小必须大于0")

    gpu_info = get_gpu_memory_info()
    if not gpu_info:
        return {"gpus": [], "total_max_tasks": 0}

    result = {
        "gpus": [],
        "total_max_tasks": 0,
        "task_memory_requirement_gib": task_memory_gib,
        "memory_buffer_gib": memory_buffer_gib,
    }

    for gpu in gpu_info:
        available_memory = gpu["memory_free_gib"] - memory_buffer_gib
        max_tasks = max(0, int(available_memory // task_memory_gib))

        gpu_result = {
            **gpu,
            "available_memory_gib": round(max(0, available_memory), 2),
            "max_tasks": max_tasks,
            "can_run_task": max_tasks > 0,
        }

        result["gpus"].append(gpu_result)
        result["total_max_tasks"] += max_tasks

    return result


def get_gpu_task_capacity(
    task_memory_gib: float, memory_buffer_gib: float = 0.5
) -> Dict[int, int]:
    """
    获取每个GPU能支持的最大任务数

    Args:
        task_memory_gib (float): 单个任务需要的显存大小(GiB)
        memory_buffer_gib (float): 预留的缓冲显存(GiB)，默认0.5GiB

    Returns:
        Dict[int, int]: 以GPU ID为键，最大任务数为值的字典
    """
    result = calculate_max_tasks_per_gpu(task_memory_gib, memory_buffer_gib)
    return {gpu["gpu_id"]: gpu["max_tasks"] for gpu in result["gpus"]}


def print_gpu_status(task_memory_gib: float, memory_buffer_gib: float = 0.5):
    """
    打印GPU状态和任务容量信息

    Args:
        task_memory_gib (float): 单个任务需要的显存大小(GiB)
        memory_buffer_gib (float): 预留的缓冲显存(GiB)
    """
    result = calculate_max_tasks_per_gpu(task_memory_gib, memory_buffer_gib)

    print(
        f"\n=== GPU 显存状态 (任务需求: {task_memory_gib}GiB, 缓冲: {memory_buffer_gib}GiB) ==="
    )
    print(
        f"{'GPU ID':<8} {'名称':<20} {'总显存':<10} {'已用':<10} {'可用':<10} {'利用率':<8} {'最大任务数':<10}"
    )
    print("-" * 85)

    for gpu in result["gpus"]:
        print(
            f"{gpu['gpu_id']:<8} {gpu['name'][:18]:<20} "
            f"{gpu['memory_total_gib']:<10} {gpu['memory_used_gib']:<10} "
            f"{gpu['available_memory_gib']:<10} {gpu['memory_utilization']:<7}% "
            f"{gpu['max_tasks']:<10}"
        )

    print("-" * 85)
    print(f"总计可运行任务数: {result['total_max_tasks']}")


def get_best_gpu_for_task(
    task_memory_gib: float, memory_buffer_gib: float = 0.5
) -> Tuple[int, Dict]:
    """
    获取最适合运行任务的GPU

    Args:
        task_memory_gib (float): 单个任务需要的显存大小(GiB)
        memory_buffer_gib (float): 预留的缓冲显存(GiB)

    Returns:
        Tuple[int, Dict]: (GPU ID, GPU信息) 如果没有合适的GPU则返回(-1, {})
    """
    result = calculate_max_tasks_per_gpu(task_memory_gib, memory_buffer_gib)

    available_gpus = [gpu for gpu in result["gpus"] if gpu["can_run_task"]]

    if not available_gpus:
        return -1, {}

    # 选择可用显存最多的GPU
    best_gpu = max(available_gpus, key=lambda x: x["available_memory_gib"])
    return best_gpu["gpu_id"], best_gpu


if __name__ == "__main__":
    # 示例使用
    task_memory = 2.0  # 假设每个任务需要2GiB显存

    print_gpu_status(task_memory)

    # 获取简化的GPU任务容量字典
    gpu_capacity = get_gpu_task_capacity(task_memory)
    print(f"\nGPU任务容量字典: {gpu_capacity}")

    gpu_id, gpu_info = get_best_gpu_for_task(task_memory)
    if gpu_id >= 0:
        print(f"\n推荐使用GPU {gpu_id}: {gpu_info['name']}")
        print(f"该GPU可运行 {gpu_info['max_tasks']} 个任务")
    else:
        print("\n当前没有GPU能运行该任务")
