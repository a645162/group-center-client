import os


def get_env_string(key: str, default_value: str = ""):
    return str(os.environ.get(key, default_value)).strip()


def get_env_int(key: str, default_value: int) -> int:
    try:
        return int(os.environ.get(key, default_value))
    except ValueError:
        return default_value
