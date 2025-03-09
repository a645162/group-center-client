from typing import Optional, Any
from enum import Enum, auto
import logging

try:
    from group_center.utils.log.backend_loguru import get_loguru_backend

    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False

from group_center.utils.log.backend_logging import get_logging_backend
from group_center.utils.log.backend_print import get_print_backend


class LogLevel(Enum):
    """日志级别枚举"""

    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class LoggerManager:
    """日志管理器单例类"""

    _instance = None
    _logger: Optional[Any] = None
    _loggers: dict = {}
    _print_mode: bool = True
    _log_level: LogLevel = LogLevel.INFO

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._initialize_logger()
        return cls._instance

    @classmethod
    def _initialize_logger(cls) -> None:
        """初始化日志记录器"""
        if cls._print_mode:
            cls._logger = get_print_backend()
        else:
            if LOGURU_AVAILABLE:
                cls._logger = get_loguru_backend()
            else:
                cls._logger = get_logging_backend()
        cls._set_log_level(cls._log_level)

    @classmethod
    def set_print_mode(cls, enabled: bool) -> None:
        """设置打印模式

        Args:
            enabled: 是否启用打印模式
        """
        cls._print_mode = enabled
        cls._initialize_logger()

    @classmethod
    def set_log_level(cls, level: LogLevel) -> None:
        """设置日志级别

        Args:
            level: 日志级别
        """
        cls._log_level = level
        cls._set_log_level(level)

    @classmethod
    def _set_log_level(cls, level: LogLevel) -> None:
        """内部方法：设置日志级别"""
        if cls._logger is not None:
            if hasattr(cls._logger, "setLevel"):
                cls._logger.setLevel(level.value)
            elif hasattr(cls._logger, "level"):
                cls._logger.level = level.value

    @classmethod
    def get_logger(
        cls, name: Optional[str] = None, config_name: Optional[str] = None
    ) -> Any:
        """获取日志记录器实例

        Args:
            name: 日志记录器名称
            config_name: 日志配置名称，用于区分不同的日志配置

        Returns:
            Any: 日志记录器实例
        """
        # 生成唯一键
        key = f"{config_name or 'default'}:{name or 'root'}"

        # 如果已有实例则直接返回
        if key in cls._loggers:
            return cls._loggers[key]

        # 初始化新实例
        if cls._logger is None:
            cls._initialize_logger()

        # 获取日志实例
        if hasattr(cls._logger, "getLogger"):
            logger = cls._logger.getLogger(name) if name else cls._logger
            if hasattr(logger, "set_config_name"):
                logger.set_config_name(config_name)
        else:
            logger = cls._logger

        # 缓存并返回
        cls._loggers[key] = logger
        return logger


def set_print_mode(enabled: bool) -> None:
    """设置打印模式

    Args:
        enabled: 是否启用打印模式
    """
    LoggerManager.set_print_mode(enabled)


def set_log_level(level: LogLevel) -> None:
    """设置日志级别

    Args:
        level: 日志级别
    """
    LoggerManager.set_log_level(level)


def get_logger(name: Optional[str] = None, config_name: Optional[str] = None) -> Any:
    """获取日志记录器

    Args:
        name: 日志记录器名称
        config_name: 日志配置名称

    Returns:
        Any: 日志记录器实例
    """
    return LoggerManager.get_logger(name, config_name)
