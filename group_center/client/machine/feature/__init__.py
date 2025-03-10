# """Group Center 机器功能模块
# Group Center Machine Feature Module
#
# 该模块提供了群组管理的机器功能扩展，包括：
# This module provides machine feature extensions for group management, including:
# - 添加用户 / Add user
# - SSH 功能 / SSH functionalities
# - 用户消息 / User messages
# """

__all__ = [
    "add_user",  # 添加用户模块 / Add user module
    "ssh",  # SSH 功能模块 / SSH functionality module
]

from . import (
    add_user,  # 添加用户模块 / Add user module
    ssh,  # SSH 功能模块 / SSH functionality module
)
