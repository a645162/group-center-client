"""Group Center 核心功能模块
Group Center Core Feature Module

该模块提供了群组管理的核心功能扩展，包括：
This module provides core feature extensions for group management, including:
- 用户文件备份 / User file backup
- 自定义客户端消息 / Custom client messages
- 远程配置 / Remote configuration
"""

__all__ = [
    "backup_user_file",  # 用户文件备份模块 / User file backup module
    "custom_client_message",  # 自定义客户端消息模块 / Custom client message module
    "machine_message",  # 机器消息模块 / Machine message module
    "remote_config",  # 远程配置模块 / Remote config module
]

from . import (
    backup_user_file,  # 用户文件备份模块 / User file backup module
    custom_client_message,  # 自定义客户端消息模块 / Custom client message module
    machine_message,  # 机器消息模块 / Machine message module
    remote_config,  # 远程配置模块 / Remote config module
)
