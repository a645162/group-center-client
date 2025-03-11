import os
from typing import Optional
from pathlib import Path
from functools import lru_cache
import json

from group_center.utils.envs import get_env_string


class RTSPConfig:
    """RTSP 配置管理类
    RTSP Configuration Management Class
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """加载配置文件
        Load configuration file
        """
        self._config_path = Path(os.getenv("RTSP_CONFIG_PATH", "/etc/rtsp/config.json"))
        self._config = {}
        if self._config_path.exists():
            try:
                with open(self._config_path, "r") as f:
                    self._config = json.load(f)
            except Exception:
                self._config = {}

    @lru_cache(maxsize=32)
    def get_rtsp_server(self) -> str:
        """获取 RTSP 服务器地址
        Get RTSP server address

        Returns:
            str: RTSP 服务器地址 / RTSP server address
        """
        # 优先从环境变量获取
        # First try to get from environment variables
        server = get_env_string("RTSP_SERVER_URL")
        if server:
            return server

        # 从配置文件获取
        # Then try to get from config file
        return self._config.get("server", "")

    def get_rtsp_port(self) -> int:
        """获取 RTSP 端口
        Get RTSP port

        Returns:
            int: RTSP 端口号 / RTSP port number
        """
        return int(self._config.get("port", 554))

    def get_rtsp_timeout(self) -> int:
        """获取 RTSP 超时时间
        Get RTSP timeout

        Returns:
            int: 超时时间（秒） / Timeout in seconds
        """
        return int(self._config.get("timeout", 30))

    def get_rtsp_auth(self) -> Optional[dict]:
        """获取 RTSP 认证信息
        Get RTSP authentication information

        Returns:
            Optional[dict]: 认证信息字典，包含username和password / Authentication info dict containing username and password
        """
        return self._config.get("auth")


@lru_cache(maxsize=2)
def get_rtsp_server() -> str:
    """获取 RTSP 服务器地址
    Get RTSP server address

    Returns:
        str: RTSP 服务器地址
        str: RTSP server address
    """
    return RTSPConfig().get_rtsp_server()
