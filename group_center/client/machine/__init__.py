# """Group Center 机器客户端模块
# Group Center Machine Client Module
#
# 该模块提供了群组管理的机器客户端功能，包括：
# This module provides machine client functionalities for group management, including:
# - SSH 帮助 / SSH assistance
# - 用户管理 / User management
# - 功能扩展 / Feature extensions
# """

"""
Group Center 机器客户端模块 / Group Center Machine Client Module

该模块提供了群组管理的机器客户端功能，包括：
This module provides machine client functionalities for group management, including:
- SSH 帮助 / SSH assistance
- 用户管理 / User management
- 功能扩展 / Feature extensions
"""

from typing import List

__all__: List[str] = [
    "ssh_helper",  # SSH 帮助模块 / SSH helper module
    "user_manager",  # 用户管理模块 / User manager module
    "feature",  # 功能模块 / Feature module
]

from . import (
    ssh_helper,  # SSH 帮助模块 / SSH helper module
    user_manager,  # 用户管理模块 / User manager module
    feature,  # 功能模块 / Feature module
)
