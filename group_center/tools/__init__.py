"""Group Center 工具模块
Group Center Tools Module

该模块提供了群组管理的工具功能，包括：
This module provides tool functionalities for group management, including:
- 深度学习模块 / Deep Learning module
- RTSP 推流 / RTSP streaming

RTSP模块需要额外的依赖，因此不可以随便加载！
RTSP module requires additional dependencies, so it cannot be loaded casually!
"""

__all__ = [
    "dl",  # 深度学习模块 / Deep Learning module
    # "rtsp",  # RTSP 推流模块 / RTSP streaming module
]

from . import (
    dl,  # 深度学习模块 / Deep Learning module
    # rtsp,  # RTSP 推流模块 / RTSP streaming module
)
