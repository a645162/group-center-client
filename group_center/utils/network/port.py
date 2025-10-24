import os
import sys
import socket
import re
from typing import List


def _check_port_windows(port: int) -> bool:
    """Windows系统下检查端口是否可用"""
    command = f"netstat -an | findstr :{port}"
    result = os.popen(command).read()
    return result == ""


def _check_port_macos(port: int) -> bool:
    """macOS系统下检查端口是否可用"""
    command = f"lsof -i :{port}"
    result = os.popen(command).read()
    return result == ""


def _check_port_linux(port: int) -> bool:
    """Linux系统下检查端口是否可用"""
    # 优先使用ss命令检查端口（更现代的工具）
    command = f"ss -tuln | grep :{port}"
    result = os.popen(command).read()
    if result:  # 如果有输出，说明端口被占用
        return False

    # 如果ss命令不可用，尝试使用netstat命令
    command = f"netstat -tuln | grep :{port}"
    result = os.popen(command).read()
    if result:
        return False

    # 最后尝试lsof命令 / Finally try the lsof command
    # Ubuntu 24.04好像就不太好用了，但是，还是留着吧，作为最后一道防线。
    command = f"lsof -i :{port}"
    result = os.popen(command).read()

    return result == ""


def _check_port_socket_binding(port: int) -> bool:
    """使用socket方式检查端口是否可用
    Check if a port is available using socket binding method

    Args:
        port (int): 要检查的端口号 / Port number to check

    Returns:
        bool: 如果端口可绑定返回True，否则返回False / True if port can be bound, False if occupied
    """
    try:
        # 创建socket对象 / Create socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置socket重用地址选项 / Set socket to reuse address
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 尝试绑定端口 / Try to bind to the port
        sock.bind(("localhost", port))
        # 绑定成功，关闭socket / Binding successful, close the socket
        sock.close()
        return True
    except socket.error:
        # 端口被占用，无法绑定 / Port is occupied, cannot bind
        return False


def check_port(port: int, use_socket_verification=False) -> bool:
    """检查端口是否可用（使用Linux/Windows/macOS命令）
    Check if a port is available using Linux/Windows/macOS command

    Args:
        port (int): 端口号 / The port number to check
        use_socket_verification (bool): 是否使用socket进行二次验证 / Whether to use socket binding for verification

    Returns:
        bool: 如果端口可用返回True，否则返回False / True if available, False otherwise
    """
    # 根据系统平台选择适当的命令行检查方法 / Select appropriate command line method based on platform
    if sys.platform == "win32":
        cmd_port_available = _check_port_windows(port)
    elif sys.platform == "darwin":  # macOS系统 / macOS system
        cmd_port_available = _check_port_macos(port)
    else:  # Linux系统 / Linux system
        cmd_port_available = _check_port_linux(port)

    # 如果命令行检查显示端口可用，根据参数决定是否再使用socket进行验证
    # If command line check shows port is available, optionally verify with socket binding
    if cmd_port_available and use_socket_verification:
        return _check_port_socket_binding(port)

    # 返回命令行检查结果 / Return command line check result
    return cmd_port_available


def _get_pid_by_port_windows(port: int) -> List[int]:
    """Windows下获取端口占用的pid"""
    pids = set()
    command = f"netstat -ano | findstr :{port}"
    result = os.popen(command).read()
    for line in result.splitlines():
        parts = line.split()
        if len(parts) >= 5:
            pid = parts[-1]
            if pid.isdigit():
                pids.add(int(pid))
    return list(pids)


def _get_pid_by_port_macos(port: int) -> List[int]:
    """macOS下获取端口占用的pid"""
    pids = set()
    command = f"lsof -i :{port}"
    result = os.popen(command).read()
    for line in result.splitlines():
        if line.startswith("COMMAND"):
            continue
        parts = line.split()
        if len(parts) >= 2 and parts[1].isdigit():
            pids.add(int(parts[1]))
    return list(pids)


def _get_pid_by_port_linux(port: int) -> List[int]:
    """Linux下获取端口占用的pid"""
    pids = set()
    # ss命令
    command = "ss -tulnp"
    result = os.popen(command).read()
    for line in result.splitlines():
        if f":{port} " in line or f":{port}\n" in line or f":{port} " in line:
            pid_matches = re.findall(r"pid=(\d+)", line)
            for pid in pid_matches:
                pids.add(int(pid))
    # netstat命令兜底
    if not pids:
        command = "netstat -tulnp"
        result = os.popen(command).read()
        for line in result.splitlines():
            if f":{port} " in line or f":{port}\n" in line or f":{port} " in line:
                pid_matches = re.findall(r"/(\d+)", line)
                for pid in pid_matches:
                    pids.add(int(pid))
    # lsof命令兜底
    if not pids:
        command = f"lsof -i :{port}"
        result = os.popen(command).read()
        for line in result.splitlines():
            if line.startswith("COMMAND"):
                continue
            parts = line.split()
            if len(parts) >= 2 and parts[1].isdigit():
                pids.add(int(parts[1]))
    return list(pids)


def get_pid_by_port(port: int) -> List[int]:
    """获取占用指定端口的所有进程pid
    Get all PIDs occupying the specified port

    Args:
        port (int): 端口号

    Returns:
        list[int]: 占用该端口的所有pid列表
    """
    if sys.platform == "win32":
        return _get_pid_by_port_windows(port)
    elif sys.platform == "darwin":
        return _get_pid_by_port_macos(port)
    else:
        return _get_pid_by_port_linux(port)


if __name__ == "__main__":
    port_list = [
        80,
        8080,
        22,
        29500,
        29501,
        29800,
        29900,
    ]

    for port in port_list:
        print(f"port {port} is available: {check_port(port)}")

    pid_list: List[int] = get_pid_by_port(8080)
    print(f"Port 8080 is occupied by PIDs: {pid_list}")
