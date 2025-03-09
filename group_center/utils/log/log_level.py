from enum import Enum, auto
from typing import Dict, Optional
import logging


class LogLevel(Enum):
    """日志级别枚举"""

    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()
    SUCCESS = auto()

    @property
    def level_name(self) -> str:
        """获取日志级别名称"""
        return self.name

    @property
    def foreground_color(self) -> str:
        """获取前景色"""
        return {
            "DEBUG": "cyan",
            "INFO": "white",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "magenta",
            "SUCCESS": "green",
        }[self.name]

    @property
    def background_color(self) -> str:
        """获取背景色"""
        return {
            "DEBUG": "",
            "INFO": "",
            "WARNING": "",
            "ERROR": "",
            "CRITICAL": "",
            "SUCCESS": "",
        }[self.name]

    @property
    def level_color(self) -> str:
        """获取级别颜色"""
        return self.foreground_color

    @classmethod
    def from_str(cls, level_str: str) -> Optional["LogLevel"]:
        """从字符串转换日志级别

        Args:
            level_str: 日志级别字符串

        Returns:
            日志级别枚举值，如果无效返回None
        """
        try:
            return cls[level_str.upper()]
        except KeyError:
            return None


class LogColorConfig:
    """日志颜色配置"""

    def __init__(
        self,
        level_color: str = "",
        foreground_color: str = "",
        background_color: str = "",
    ):
        self.level_color = level_color
        self.foreground_color = foreground_color
        self.background_color = background_color


class LogLevelManager:
    """日志级别管理器"""

    _instance = None
    _level_colors: Dict[LogLevel, LogColorConfig] = {
        LogLevel.DEBUG: LogColorConfig(level_color="blue", foreground_color="blue"),
        LogLevel.INFO: LogColorConfig(),
        LogLevel.WARNING: LogColorConfig(
            level_color="yellow", foreground_color="yellow"
        ),
        LogLevel.ERROR: LogColorConfig(level_color="red", foreground_color="red"),
        LogLevel.CRITICAL: LogColorConfig(
            level_color="cyan", foreground_color="cyan", background_color="on_red"
        ),
        LogLevel.SUCCESS: LogColorConfig(level_color="green", foreground_color="green"),
    }
    _current_level: LogLevel = LogLevel.INFO

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def set_level(cls, level: LogLevel) -> None:
        """设置当前日志级别

        Args:
            level: 要设置的日志级别
        """
        cls._current_level = level

    @classmethod
    def get_level(cls) -> LogLevel:
        """获取当前日志级别

        Returns:
            当前日志级别
        """
        return cls._current_level

    @classmethod
    def get_color_config(cls, level: LogLevel) -> LogColorConfig:
        """获取日志级别对应的颜色配置

        Args:
            level: 日志级别

        Returns:
            日志颜色配置
        """
        return cls._level_colors.get(level, LogColorConfig())

    @classmethod
    def to_logging_level(cls, level: LogLevel) -> int:
        """将日志级别转换为logging模块的级别

        Args:
            level: 日志级别

        Returns:
            logging模块对应的级别值
        """
        level_map = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL,
        }
        return level_map.get(level, logging.INFO)


def get_log_level() -> LogLevel:
    """获取当前日志级别

    Returns:
        当前日志级别
    """
    return LogLevelManager.get_level()
