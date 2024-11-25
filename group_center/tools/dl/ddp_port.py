import os
import sys


def check_port(port: int) -> bool:
    # Use Linux command to check port
    command = f"lsof -i:{port}"
    result = os.popen(command).read()
    return result == ""


def get_torch_distributed_port() -> int:
    port = 29500

    if sys.platform != "linux":
        return port

    while not check_port(port):
        port += 1
    return port


def main():
    print(get_torch_distributed_port())


if __name__ == "__main__":
    main()
