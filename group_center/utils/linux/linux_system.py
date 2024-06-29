import platform


def is_run_on_linux():
    return platform.system() == "Linux"
