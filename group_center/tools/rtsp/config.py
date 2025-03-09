import os
from typing import Optional
from pathlib import Path
from functools import lru_cache
import json

from group_center.utils.envs import get_env_string


class RTSPConfig:
    """RTSP 配置管理类"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """加载配置文件"""
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
        
        Returns:
            str: RTSP 服务器地址
        """
        # 优先从环境变量获取
        server = get_env_string("RTSP_SERVER_URL")
        if server:
            return server
            
        # 从配置文件获取
        return self._config.get("server", "")

    def get_rtsp_port(self) -> int:
        """获取 RTSP 端口
        
        Returns:
            int: RTSP 端口号
        """
        return int(self._config.get("port", 554))

    def get_rtsp_timeout(self) -> int:
        """获取 RTSP 超时时间
        
        Returns:
            int: 超时时间（秒）
        """
        return int(self._config.get("timeout", 30))

    def get_rtsp_auth(self) -> Optional[dict]:
        """获取 RTSP 认证信息
        
        Returns:
            Optional[dict]: 认证信息字典，包含username和password
        """
        return self._config.get("auth")


@lru_cache(maxsize=2)
def get_rtsp_server() -> str:
    """获取 RTSP 服务器地址
    
    Returns:
        str: RTSP 服务器地址
    """
    return RTSPConfig().get_rtsp_server()
