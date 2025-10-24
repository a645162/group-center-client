import os

try:
    from typing import Final
except ImportError:
    from typing_extensions import Final

# 当前 Python 文件路径 / Current Python file path
current_py_path: Final[str] = os.path.abspath(__file__)

# 全局配置文件目录路径 / Global configuration file directory path
path_dir_config_global: Final[str] = os.path.dirname(current_py_path)

# 项目根目录路径 / Project root directory path
path_dir_base: Final[str] = os.path.dirname(path_dir_config_global)

# 主包根目录路径 / Package root directory path
package_dir_base: Final[str] = os.path.join(path_dir_base, "group_center")

# 配置文件目录路径 / Configuration directory path
path_dir_config: Final[str] = os.path.join(package_dir_base, "config")

if __name__ == "__main__":
    print(path_dir_base)
