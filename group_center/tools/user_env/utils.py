import sys


def get_python_version() -> str:
    """获取Python版本字符串 (Get Python version string)
    Get Python version string

    Returns:
        str: Python版本字符串 (Python version string)
        str: Python version string
    """
    version_str = sys.version.split()[0].strip()
    return version_str


PythonVersion = get_python_version()
