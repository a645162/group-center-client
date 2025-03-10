#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test suite initialization."""

import unittest
from pathlib import Path


def run_tests():
    """Run all tests.
    运行所有测试
    """
    test_dir = Path("test")
    discovery = unittest.defaultTestLoader.discover(test_dir)
    runner = unittest.TextTestRunner()
    runner.run(discovery)


if __name__ == "__main__":
    run_tests()
