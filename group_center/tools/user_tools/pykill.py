import argparse
import os
import psutil

from group_center.utils.process.process import (
    get_top_python_process_pid,
    check_is_python_process,
)


def kill_process(pid: int):
    try:
        proc = psutil.Process(pid)
        proc.kill()
        print(f"Killed process {pid}")
    except Exception as e:
        print(f"Failed to kill process {pid}: {e}")


def kill_by_pid(pid: int):
    top_pid = get_top_python_process_pid(pid)
    if top_pid == -1:
        # 如果父进程链中没有python进程，检查当前pid是否为python进程
        if check_is_python_process(pid):
            print("No python process found in parent chain, killing current process.")
            kill_process(pid)
        else:
            print(
                "No python process found in chain and current process is not python, skipping."
            )
        return
    kill_process(top_pid)


def kill_by_user(username: str):
    current_pid = os.getpid()
    for proc in psutil.process_iter(["pid", "username"]):
        pid = proc.info["pid"]
        user = proc.info["username"]
        if user == username and check_is_python_process(pid) and pid != current_pid:
            kill_process(pid)


def main():
    parser = argparse.ArgumentParser(
        description="Kill python processes by pid or user."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--pid", type=int, help="Target process id")
    group.add_argument("--user", type=str, help="Target username")
    args = parser.parse_args()

    if args.pid is not None:
        print(f"Attempting to kill process with pid: {args.pid}")
        kill_by_pid(args.pid)
    elif args.user is not None:
        print(f"Attempting to kill processes for user: {args.user}")
        kill_by_user(args.user)
    else:
        print("Please specify either --pid or --user argument.")


if __name__ == "__main__":
    main()
