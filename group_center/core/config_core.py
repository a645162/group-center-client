from typing import Optional, List
from dataclasses import dataclass

from group_center.utils.envs import (
    get_env_string,
)  # 环境变量工具 / Environment variable utility


@dataclass
class MachineConfig:
    """机器配置数据类
    Machine configuration data class

    Attributes:
        url (str): 服务器URL / Server URL
        name_full (str): 完整机器名 / Full machine name
        name_short (str): 简短机器名 / Short machine name
        password (str): 认证密码 / Authentication password
    """

    url: str
    name_full: str
    name_short: str
    password: str


def get_env_machine_config() -> Optional[MachineConfig]:
    """从环境变量获取机器配置
    Get machine configuration from environment variables

    Returns:
        Optional[MachineConfig]: 包含机器配置的对象，如果配置不完整则返回None
        Machine configuration object, returns None if configuration is incomplete

    Raises:
        ValueError: 如果缺少必要的配置项
        If required configuration items are missing
    """

    def get_required_env(keys: List[str]) -> Optional[str]:
        """获取必需的环境变量
        Get required environment variable

        Args:
            keys (List[str]): 环境变量键列表，按顺序尝试
            List of environment variable keys to try in order

        Returns:
            Optional[str]: 环境变量值，如果所有键都未设置则返回None
            Environment variable value, returns None if none of the keys are set
        """
        for key in keys:
            value: Optional[str] = get_env_string(key)
            if value:
                return value
        return None

    try:
        # 获取配置项 / Get configuration items
        url: Optional[str] = get_required_env(["GROUP_CENTER_URL"])
        name_full: Optional[str] = get_required_env(["GROUP_CENTER_MACHINE_NAME"])
        name_short: Optional[str] = get_required_env(
            ["GROUP_CENTER_MACHINE_NAME_SHORT", "SERVER_NAME_SHORT"]
        )
        password: Optional[str] = get_required_env(
            [
                "GROUP_CENTER_MACHINE_PASSWORD",
                "GROUP_CENTER_PASSWORD",
            ]
        )

        # 验证配置完整性 / Validate configuration completeness
        if not all([url, name_full, name_short, password]):
            return None

        return MachineConfig(
            url=url, name_full=name_full, name_short=name_short, password=password
        )
    except ValueError:
        return None


if __name__ == "__main__":
    try:
        config: Optional[MachineConfig] = get_env_machine_config()
        print(config)
    except ValueError as e:
        print(f"Configuration error: {e}")
