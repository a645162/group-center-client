import os
import tempfile


def get_env_string(key: str, default_value: str = ""):
    return str(os.environ.get(key, default_value)).strip()


def get_env_int(key: str, default_value: int) -> int:
    try:
        return int(os.environ.get(key, default_value))
    except ValueError:
        return default_value


def get_user_home_dir() -> str:
    return os.path.expanduser("~")


def get_base_tmp_dir() -> str:
    return tempfile.gettempdir()


def get_a_tmp_dir() -> str:
    dir_path = tempfile.mkdtemp()

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    return dir_path


if __name__ == "__main__":
    # print(get_env_string("PATH"))
    # print(get_env_int("PATH", 0))
    print(get_user_home_dir())
    print(get_base_tmp_dir())
    print(get_a_tmp_dir())
