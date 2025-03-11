import argparse
import subprocess
import sys
import os

from config.global_config import path_dir_config


def install_requirements(requirements_path: str) -> None:
    """
    Install Python requirements from specified file.
    从指定文件安装Python依赖

    Args:
        requirements_path (str): Path to requirements file / requirements文件路径
    """
    if not os.path.exists(requirements_path):
        requirements_path = os.path.join(path_dir_config, requirements_path)

    if not os.path.exists(requirements_path):
        print(f"Requirements file {requirements_path} not found")
        sys.exit(1)

    try:
        subprocess.run(["pip", "install", "-r", requirements_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements from {requirements_path}: {e}")
        sys.exit(1)


def main() -> None:
    """
    Main function for installing dependencies.
    安装依赖的主函数
    """
    parser = argparse.ArgumentParser(
        description="Dependency installation script for group-center-client. / group-center-client的依赖安装脚本"
    )

    parser.add_argument(
        "--no-gui",
        help="Skip installation of GUI dependencies. / 跳过GUI依赖的安装",
        action="store_true",
    )

    args = parser.parse_args()

    print("Installing base dependencies...")
    install_requirements("requirements.txt")

    print("Installing development dependencies...")
    install_requirements("r-dev-requirements.txt")

    print("Installing Computer Vision dependencies...")
    install_requirements("r-cv-requirements.txt")

    # Check Python is higher than 3.7
    if not sys.version_info < (3, 7):
        os.system("pip install ruff")

    if not args.no_gui:
        print("Installing GUI dependencies...")
        install_requirements("r-gui-requirements.txt")

    ret = os.system("pip install -e .")
    if ret != 0:
        print("Error installing group-center-client")
        sys.exit(1)

    print("Installation completed.")


if __name__ == "__main__":
    main()
