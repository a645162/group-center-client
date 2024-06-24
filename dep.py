import argparse
import subprocess
import sys

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

    if not args.no_gui:
        print("Installing GUI dependencies...")
        install_requirements("./config/r-gui-requirements.txt")
    print("Installation completed.")


if __name__ == "__main__":
    main()
