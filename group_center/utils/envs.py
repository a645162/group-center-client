import os


def get_env_string(key: str, default_value: str = ""):
    return str(os.environ.get(key, default_value)).strip()
