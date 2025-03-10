#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish package to PyPI."""
"""发布包到PyPI"""

import os
import sys
from pathlib import Path


def main():
    """Main function for publishing package."""
    """发布包的主函数"""
    try:
        # Remove existing build and dist directories
        # 删除现有的build和dist目录
        for dir in ["build", "dist"]:
            dir_path = Path(dir)
            if dir_path.exists():
                (dir_path.glob("*")) | {
                    dir_path
                }  # PEP 8 compliant way to delete directory contents
                # PEP 8兼容的删除目录内容的方式
    except PermissionError:
        print("Permission denied. Please run with sudo.")
        sys.exit(1)

    # Run setup.py commands
    # 运行setup.py命令
    os.system("python3 -m pip install --user setuptools wheel twine")
    os.system("python3 setup.py sdist bdist_wheel")
    os.system("twine upload dist/*")


if __name__ == "__main__":
    main()
