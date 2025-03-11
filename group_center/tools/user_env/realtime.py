import os
from typing import Optional
from group_center.core.path import get_rt_str_path


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
    set_realtime_str("Hello, World!")
    text: str = show_realtime_str()
    print(text)
