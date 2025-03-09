from typing import Tuple, Optional
from dataclasses import dataclass

from group_center.utils.envs import get_env_string


@dataclass
class MachineConfig:
    """机器配置数据类"""

    url: str
    name_full: str
    name_short: str
    password: str


def get_env_machine_config() -> MachineConfig:
    """从环境变量获取机器配置

    Returns:
        MachineConfig: 包含机器配置的对象

    Raises:
        ValueError: 如果缺少必要的配置项
    """

    def get_required_env(keys: list[str]) -> Optional[str]:
        """获取必需的环境变量

        Args:
            keys: 环境变量键列表，按顺序尝试

        Returns:
            Optional[str]: 环境变量值，如果所有键都未设置则返回None
        """
        for key in keys:
            value = get_env_string(key)
            if value:
                return value
        return None

    try:
        url = get_required_env(["GROUP_CENTER_URL"])
        name_full = get_required_env(["GROUP_CENTER_MACHINE_NAME"])
        name_short = get_required_env(
            ["GROUP_CENTER_MACHINE_NAME_SHORT", "SERVER_NAME_SHORT"]
        )
        password = get_required_env(
            [
                "GROUP_CENTER_MACHINE_PASSWORD",
                "GROUP_CENTER_PASSWORD",
            ]
        )
        
        # print(url, name_full, name_short, password)
        if not all([url, name_full, name_short, password]):
            return None

        return MachineConfig(
            url=url, name_full=name_full, name_short=name_short, password=password
        )
    except ValueError as e:
        return None


if __name__ == "__main__":
    try:
        config = get_env_machine_config()
        print(config)
    except ValueError as e:
        print(f"Configuration error: {e}")
