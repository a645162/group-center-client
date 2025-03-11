"""配置模块
Configuration Module

该模块提供了项目配置相关的功能，包括：
This module provides project configuration related functionalities, including:
- 全局配置 / Global configuration
- 版本管理 / Version management
- 路径管理 / Path management
"""

from typing import List

__all__: List[str] = [
    "global_config",  # 全局配置模块 / Global configuration module
    "version",  # 版本管理模块 / Version management module
]

from . import (
    global_config,  # 全局配置模块 / Global configuration module
    version,  # 版本管理模块 / Version management module
)

from .version import __version__  # noqa: F401
