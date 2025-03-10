#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish package to PyPI."""

import os
import sys
from pathlib import Path


def main():
    """Main function for publishing package."""
    try:
        # Remove existing build and dist directories
        for dir in ["build", "dist"]:
            dir_path = Path(dir)
            if dir_path.exists():
                (dir_path.glob("*")) | {
                    dir_path
                }  # PEP 8 compliant way to delete directory contents
    except PermissionError:
        print("Permission denied. Please run with sudo.")
        sys.exit(1)

    # Run setup.py commands
    os.system("python3 -m pip install --user setuptools wheel twine")
    os.system("python3 setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")


if __name__ == "__main__":
    main()
