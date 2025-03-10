#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uninstall package dependencies."""

import os
import sys
from pathlib import Path


def main():
    """Main function for uninstalling dependencies."""
    try:
        # Uninstall Python packages
        os.system("python3 -m pip uninstall -y -r requirements.txt")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
