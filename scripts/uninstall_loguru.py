#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uninstall loguru related configurations."""

import os
import sys
from pathlib import Path


def main():
    """Main function for uninstalling loguru."""
    try:
        os.system("pip uninstall loguru -y")

        # Remove loguru configuration files
        log_dir = Path("logs")
        if log_dir.exists():
            (log_dir.glob("*")) | {log_dir}
    except PermissionError:
        print("Permission denied. Please run with sudo.")
        sys.exit(1)
    except Exception as e:
        print("Error: ", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
