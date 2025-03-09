import os
import re
import sys


def RUN_COMMAND() -> str:
    """获取当前运行命令 (Get current run command)

    Returns:
        str: 当前执行的命令字符串
    """
    return " ".join(sys.argv).strip()


def CONDA_ENV_NAME() -> str:
    """获取当前Conda环境名称 (Get current Conda environment name)

    Returns:
        str: Conda环境名称 (Conda environment name)
    """
    run_command = RUN_COMMAND()
    pattern = r"envs/(.*?)/bin/python "
    match = re.search(pattern, run_command)
    if match:
        conda_env_name = match.group(1)
        env_str = conda_env_name
    else:
        env_str = os.getenv("CONDA_DEFAULT_ENV", "")

    env_str = env_str.strip() or "base"
    return env_str
