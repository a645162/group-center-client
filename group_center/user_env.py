import os
import re
import sys
from typing import List


def PythonVersion() -> str:
    version_str: str = str(sys.version)

    spilt_list: List[str] = version_str.split("|")

    version_str = spilt_list[0].strip()

    return version_str


def ENV_SCREEN_NAME_FULL() -> str:
    return os.getenv("STY", "").strip()


def ENV_SCREEN_SESSION_ID() -> str:
    spilt_list: List[str] = ENV_SCREEN_NAME_FULL().split(".")

    if len(spilt_list) < 2:
        return ""

    return spilt_list[0].strip()


def ENV_SCREEN_SESSION_NAME() -> str:
    spilt_list: List[str] = ENV_SCREEN_NAME_FULL().split(".")

    if len(spilt_list) < 2:
        return ""

    spilt_list = spilt_list[1:]

    return ".".join(spilt_list).strip()


def is_in_screen_session() -> bool:
    return ENV_SCREEN_SESSION_NAME() != ""


def ENV_CUDA_ROOT():
    cuda_home: str = os.getenv("CUDA_HOME", "").strip()
    nvcc_path: str = os.path.join(cuda_home, "bin", "nvcc")

    cuda_nvcc_bin: str = ""

    if os.path.exists(nvcc_path):
        cuda_nvcc_bin = nvcc_path
    else:
        cuda_toolkit_root = os.getenv("CUDAToolkit_ROOT", "").strip()
        nvcc_path = os.path.join(cuda_toolkit_root, "bin", "nvcc")
        if os.path.exists(nvcc_path):
            cuda_nvcc_bin = nvcc_path

    return cuda_nvcc_bin


def CUDA_VERSION(nvcc_path: str = "") -> str:
    nvcc_path = nvcc_path.strip()
    if nvcc_path == "" or (not os.path.exists(nvcc_path)):
        nvcc_path = ENV_CUDA_ROOT()
    if nvcc_path == "":
        return ""

    cuda_version: str = ""

    try:
        result = os.popen(f"{nvcc_path} --version").read()
        if "release" not in result:
            return ""
        result_list = result.split("\n")
        version: str = ""
        for line in result_list:
            if "release" in line:
                version = line.split(",")[-1].strip()
                break

        cuda_version = str(version).strip().lower().replace("v", "")
    except Exception:
        return ""

    return cuda_version


def ENV_CUDA_LOCAL_RANK() -> str:
    return os.getenv("LOCAL_RANK", "").strip()


def ENV_CUDA_WORLD_SIZE() -> str:
    return os.getenv("LOCAL_WORLD_SIZE", "").strip()


def cuda_local_rank() -> int:
    local_rank = ENV_CUDA_LOCAL_RANK().strip()
    if local_rank == "":
        return -1
    try:
        return int(local_rank)
    except Exception:
        return -1


def cuda_world_size() -> int:
    world_size = ENV_CUDA_WORLD_SIZE().strip()
    if world_size == "":
        return -1
    try:
        return int(world_size)
    except Exception:
        return -1


def is_first_card_process() -> bool:
    if cuda_world_size() < 2:
        return True

    return cuda_local_rank() == 0


def RUN_COMMAND() -> str:
    return " ".join(sys.argv).strip()


def CONDA_ENV_NAME() -> str:
    run_command = RUN_COMMAND()

    pattern = r"envs/(.*?)/bin/python "
    match = re.search(pattern, run_command)
    if match:
        conda_env_name = match.group(1)
        env_str = conda_env_name
    else:
        env_str = os.getenv("CONDA_DEFAULT_ENV", "")

    env_str = env_str.strip()

    if env_str == "":
        env_str = "base"

    return env_str


def set_epoch_str(epoch_str: str) -> None:
    # Set Env "GROUP_CENTER_USER_ENV_EPOCH"
    os.environ["GROUP_CENTER_USER_ENV_EPOCH"] = epoch_str


if __name__ == "__main__":
    print(PythonVersion())

    print(ENV_SCREEN_NAME_FULL())
    print(ENV_SCREEN_SESSION_ID())
    print(ENV_SCREEN_SESSION_NAME())

    print(ENV_CUDA_ROOT())
    print(CUDA_VERSION())

    print(ENV_CUDA_LOCAL_RANK())
    print(ENV_CUDA_WORLD_SIZE())

    print(RUN_COMMAND())
    print(CONDA_ENV_NAME())
