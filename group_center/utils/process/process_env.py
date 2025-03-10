import os
import sys
from typing import List

from group_center.utils.process.process import (
    get_chain_of_process,
    get_parent_process_pid,
    get_process_name,
    get_process_name_list,
    get_process_path,
)
from group_center.utils.string.keywords import contains_any_keywords


def check_parent_process_name_keywords(keywords: List[str]) -> bool:
    """
    检查父进程名称是否包含指定的关键字。
    Check if parent process names contain any of the specified keywords.

    Args:
        keywords (List[str]): 要检查的关键字列表 / List of keywords to check for

    Returns:
        bool: 如果任何父进程名称包含任何关键字则返回True，否则返回False
              True if any parent process name contains any keyword, False otherwise
    """
    pid_list: List[int] = get_chain_of_process(get_parent_process_pid(-1))
    p_name_list: List[str] = get_process_name_list(pid_list)

    for process_name in p_name_list:
        for keyword in keywords:
            if keyword and (keyword in process_name):
                return True

    return False


def is_run_by_gateway() -> bool:
    """
    检查当前进程是否由网关服务启动。
    Check if the current process is run by a gateway service.

    Returns:
        bool: 如果当前进程由网关服务启动则返回True，否则返回False
              True if the process is run by a gateway service, False otherwise
    """
    keywords: List[str] = ["remote-dev-serv", "launcher.sh"]
    return check_parent_process_name_keywords(keywords)


def is_run_by_vscode_remote() -> bool:
    """
    检查当前进程是否由VS Code远程服务启动。
    Check if the current process is run by VS Code remote service.

    Returns:
        bool: 如果由VS Code远程服务启动则返回True，否则返回False
              True if the process is run by VS Code remote service, False otherwise
    """
    keywords = ["code-"]
    if check_parent_process_name_keywords(keywords):
        return True

    pid_list: List[int] = get_chain_of_process(get_parent_process_pid(-1))

    for pid in pid_list:
        process_name = get_process_name(pid)
        process_path = get_process_path(pid)
        if process_name == "node":
            return contains_any_keywords(process_path, keywords)

    return False


def is_run_by_screen() -> bool:
    """
    检查当前进程是否由screen终端复用器启动。
    Check if the current process is run by screen terminal multiplexer.

    Returns:
        bool: 如果由screen启动则返回True，否则返回False
              True if the process is run by screen, False otherwise
    """
    keywords = ["screen"]
    return check_parent_process_name_keywords(keywords)


def is_run_by_tmux() -> bool:
    """
    检查当前进程是否由tmux终端复用器启动。
    Check if the current process is run by tmux terminal multiplexer.

    Returns:
        bool: 如果由tmux启动则返回True，否则返回False
              True if the process is run by tmux, False otherwise
    """
    keywords = ["tmux"]
    return check_parent_process_name_keywords(keywords)


def is_debug_mode() -> bool:
    """
    检查当前环境是否处于调试模式。
    Check if the current environment is in debug mode.

    Returns:
        bool: 如果处于调试模式则返回True，否则返回False
              True if in debug mode, False otherwise.
    """

    if is_run_by_screen():
        return False

    if sys.gettrace():
        return True

    if is_run_by_gateway() or is_run_by_vscode_remote():
        return True

    debug_str = os.getenv("DEBUG")
    if debug_str is None:
        debug_str = ""

    return debug_str.lower() == "true" or debug_str == "1"


if __name__ == "__main__":
    print("is_run_by_gateway", is_run_by_gateway())
    print("is_run_by_vscode_remote", is_run_by_vscode_remote())
    print("is_run_by_screen", is_run_by_screen())
    print("is_run_by_tmux", is_run_by_tmux())
