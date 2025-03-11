import os
import sys


def check_port(port: int) -> bool:
    """检查端口是否可用（使用Linux/Windows/macOS命令）
    Check if a port is available using Linux/Windows/macOS command


    Args:
        port (int): 端口号/The port number to check

    Returns:
        bool: 如果端口可用返回True，否则返回False/True if available, False otherwise
    """
    if sys.platform == "win32":
        # Windows系统下使用netstat命令检查端口
        command = f"netstat -an | findstr :{port}"
        result = os.popen(command).read()
        return result == ""
    elif sys.platform == "darwin":  # macOS系统
        # macOS系统下使用lsof命令检查端口
        command = f"lsof -i :{port}"
        result = os.popen(command).read()
        return result == ""
    else:
        # Linux系统下使用lsof命令检查端口
        command = f"lsof -i:{port}"
        result = os.popen(command).read()
        return result == ""


def get_torch_distributed_port() -> int:
    """Get an available port for PyTorch distributed training
    获取用于PyTorch分布式训练的可用端口

    Returns:
        int: An available port number starting from 29500
        从29500开始的可用端口号
    """
    port = 29500

    if sys.platform not in ["linux", "win32", "darwin"]:
        return port

    while not check_port(port):
        port += 1
    return port


def main():
    """Main function to print the available port
    主函数，打印可用端口
    """
    print(get_torch_distributed_port())


if __name__ == "__main__":
    main()
