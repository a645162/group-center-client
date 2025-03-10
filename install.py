import argparse
import subprocess
import sys
import os

from config.version import __version__


def install_requirements(requirements_path):
    try:
        subprocess.run(["pip", "install", "-r", requirements_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements from {requirements_path}: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Dependency installation script for group-center-client."
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Skip installation of GUI dependencies.",
        action="store_true",
    )
    parser.add_argument(
        "--no-gui",
        help="Skip installation of GUI dependencies.",
        action="store_true",
    )

    args = parser.parse_args()

    if args.version:
        print("group-center-client version:" + str(__version__))
        sys.exit(0)

    print("Installing base dependencies...")
    install_requirements("./config/requirements.txt")
    print("Installing development dependencies...")
    install_requirements("./config/r-dev-requirements.txt")

    # Check Python is higher than 3.7
    if not sys.version_info < (3, 7):
        os.system("pip install ruff")

    if not args.no_gui:
        print("Installing GUI dependencies...")
        install_requirements("./config/r-gui-requirements.txt")

    ret = os.system("pip install -e .")
    if ret != 0:
        print("Error installing group-center-client")
        sys.exit(1)

    print("Installation completed.")


if __name__ == "__main__":
    main()
