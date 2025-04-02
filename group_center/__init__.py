# """Group Center 主包
# Group Center Main Package
#
# 该包提供了群组管理的核心功能，包括客户端、核心功能和用户管理等。
# This package provides core functionalities for group management, including client, core features and user management.
#
# 主要功能模块：
# - 客户端（client）：提供机器和用户的客户端功能
# - 核心功能（core）：包括配置、加密、路径管理等核心功能
# - 用户管理（user）：提供系统用户和Linux用户的管理功能
#
# 版本信息：
# {version}
# """

from .config import __version__  # noqa: F401

try:
    from . import (
        client,  # 客户端模块 / Client module
        core,  # 核心功能模块 / Core features module
        user,  # 用户管理模块 / User management module
        feature,  # 功能模块 / Feature module
        tools,  # 工具模块 / Tools module
        user_env,  # 用户环境模块 / User environment module
        user_tools,  # 用户工具模块 / User tools module
        utils,  # 工具集模块 / Utilities module
        config,  # 配置模块 / Configuration module
    )

    __all__ = [
        "client",  # 客户端模块 / Client module
        "core",  # 核心功能模块 / Core features module
        "user",  # 用户管理模块 / User management module
        "feature",  # 功能模块 / Feature module
        "tools",  # 工具模块 / Tools module
        "user_env",  # 用户环境模块 / User environment module
        "user_tools",  # 用户工具模块 / User tools module
        "utils",  # 工具集模块 / Utilities module
        "config",  # 配置模块 / Configuration module
    ]
except ImportError:
    pass
