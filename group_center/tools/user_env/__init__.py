# """Group Center 用户环境工具模块
# Group Center User Environment Tools Module
#
# 该模块提供了群组管理的用户环境相关工具，包括：
# This module provides user environment-related tools for group management, including:
# - 屏幕会话管理 / Screen session management
# - CUDA 环境信息 / CUDA environment information
# - Conda 环境信息 / Conda environment information
# - 实时信息显示 / Realtime information display
# - Python 版本获取 / Python version retrieval
# """

__all__ = [
    # Screen 会话相关
    "ENV_SCREEN_NAME_FULL",
    "ENV_SCREEN_SESSION_ID",
    "ENV_SCREEN_SESSION_NAME",
    "is_in_screen_session",
    # CUDA 相关
    "ENV_CUDA_ROOT",
    "CUDA_VERSION",
    "ENV_CUDA_LOCAL_RANK",
    "ENV_CUDA_WORLD_SIZE",
    "cuda_local_rank",
    "cuda_world_size",
    "is_first_card_process",
    # Conda 相关
    "RUN_COMMAND",
    "CONDA_ENV_NAME",
    # 实时信息显示
    "set_realtime_str",
    "show_realtime_str",
    # 工具函数
    "get_python_version",
    "PythonVersion",
]

from .screen import (
    ENV_SCREEN_NAME_FULL,
    ENV_SCREEN_SESSION_ID,
    ENV_SCREEN_SESSION_NAME,
    is_in_screen_session,
)

from .cuda import (
    ENV_CUDA_ROOT,
    CUDA_VERSION,
    ENV_CUDA_LOCAL_RANK,
    ENV_CUDA_WORLD_SIZE,
    cuda_local_rank,
    cuda_world_size,
    is_first_card_process,
)

from .conda import (
    RUN_COMMAND,
    CONDA_ENV_NAME,
)

from .realtime import (
    set_realtime_str,
    show_realtime_str,
)

from .utils import (
    get_python_version,
    PythonVersion,
)
