import sys

from group_center.utils.network.port import check_port


def get_debugpy_port() -> int:
    """Get an available port for DebugPy debugging
    获取用于DebugPy调试的可用端口

    Returns:
        int: An available port number starting from 9501
        从9501开始的可用端口号
    """
    port = 9501

    if sys.platform not in ["linux", "win32", "darwin"]:
        return port

    while not check_port(port):
        port += 1
    return port


def main():
    """Main function to print the available port
    主函数，打印可用端口
    """
    print(get_debugpy_port())


if __name__ == "__main__":
    main()
