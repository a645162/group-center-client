from typing import Optional, Any, Dict, Union, Type, TypeVar
from enum import Enum, auto
import logging
import sys

try:
    from group_center.utils.log.backend_loguru import get_loguru_backend, LoguruLogger

    LOGURU_AVAILABLE = (
        True  # Flag indicating if loguru is available / 标识loguru是否可用
    )
except ImportError:
    LOGURU_AVAILABLE = False  # Loguru not available / loguru不可用
    LoguruLogger = (
        Any  # Type alias when loguru is not available / loguru不可用时的类型别名
    )

from group_center.utils.log.backend_logging import get_logging_backend
from group_center.utils.log.backend_print import get_print_backend, BackendPrint

# 定义日志记录器类型的联合类型 | Define union type for logger instances
LoggerType = Union[logging.Logger, LoguruLogger, BackendPrint, Any]

# 定义LoggerManager类型变量，用于单例模式 | Define LoggerManager type variable for singleton pattern
T = TypeVar("T", bound="LoggerManager")


class LogLevel(Enum):
    """日志级别枚举 | Log level enumeration"""

    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


class LoggerManager:
    """日志管理器单例类（管理全局日志实例）

    单例范围说明：
    - 管理器本身是单例的，维护全局日志配置
    - 通过get_logger()获取的实例根据参数不同可能不同
    - 相同(name, config_name)组合返回相同实例
    """

    @classmethod
    def set_default_logger(cls: Type[T], logger: LoggerType) -> None:
        """设置全局默认日志记录器 | Set global default logger

        Args:
            logger (LoggerType): 日志记录器实例 | Logger instance
        """
        cls._default_logger = logger
        cls._logger = logger  # 更新_logger引用，确保后续获取logger时使用新设置的logger | Update _logger reference to ensure the new logger is used for subsequent calls
        cls._loggers.clear()  # 清除已缓存的记录器 | Clear cached loggers
        cls._set_log_level(
            cls._log_level
        )  # 重新应用日志级别 | Reapply log level to the new logger

    _instance: Optional[T] = None
    _logger: Optional[LoggerType] = None
    _default_logger: Optional[LoggerType] = (
        None  # 全局默认日志实例 | Global default logger instance
    )
    _loggers: Dict[str, LoggerType] = {}
    _print_mode: bool = True
    _log_level: LogLevel = LogLevel.INFO
    _using_custom_logger: bool = (
        False  # 标记是否使用了自定义logger | Flag indicating whether a custom logger is being used
    )
    _verbose_checked: bool = False  # 标记是否已检查过verbose参数 | Flag indicating whether verbose parameter has been checked

    def __new__(cls: Type[T]) -> T:
        """Create singleton instance / 创建单例实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._check_verbose_arg()  # 在初始化时检查verbose参数 | Check verbose argument during initialization
            cls._initialize_logger()
        return cls._instance

    @classmethod
    def _check_verbose_arg(cls: Type[T]) -> None:
        """检查命令行参数中是否包含--verbose | Check if --verbose is in command line arguments"""
        if not cls._verbose_checked:
            if '--verbose' in sys.argv or '-v' in sys.argv:
                cls._log_level = LogLevel.DEBUG
            cls._verbose_checked = True

    @classmethod
    def _initialize_logger(cls: Type[T]) -> None:
        """初始化日志记录器 | Initialize logger"""
        # 如果已经设置了自定义logger，则不再初始化 | If a custom logger is already set, skip initialization
        if cls._using_custom_logger and cls._default_logger is not None:
            return

        if cls._print_mode:
            cls._logger = get_print_backend()
        else:
            if LOGURU_AVAILABLE:
                cls._logger = get_loguru_backend()
            else:
                cls._logger = get_logging_backend()
        cls._default_logger = (
            cls._logger
        )  # 初始化默认日志实例 | Initialize default logger instance
        cls._set_log_level(cls._log_level)

    @classmethod
    def set_print_mode(cls: Type[T], enabled: bool) -> None:
        """设置打印模式 | Set print mode

        Args:
            enabled (bool): 是否启用打印模式 | Whether to enable print mode
        """
        # 如果使用自定义logger，不要切换回打印模式 | If using a custom logger, don't switch back to print mode
        if cls._using_custom_logger:
            return

        cls._print_mode = enabled
        cls._initialize_logger()

    @classmethod
    def set_log_level(cls: Type[T], level: LogLevel) -> None:
        """设置日志级别 | Set log level

        Args:
            level (LogLevel): 日志级别 | Log level
        """
        cls._log_level = level
        cls._set_log_level(level)

    @classmethod
    def _set_log_level(cls: Type[T], level: LogLevel) -> None:
        """内部方法：设置日志级别 | Internal method: Set log level

        将LogLevel枚举转换为对应字符串类型的日志级别并应用到logger实例
        Converts LogLevel enum to corresponding string log level and applies it to logger instance

        Args:
            level (LogLevel): 日志级别枚举 | Log level enumeration
        """
        if cls._default_logger is not None:
            if hasattr(cls._default_logger, "setLevel"):
                cls._default_logger.setLevel(
                    level.name
                )  # 使用枚举名称作为字符串级别 | Use enum name as string level
            elif hasattr(cls._default_logger, "level"):
                cls._default_logger.level = (
                    level.name
                )  # 对于loguru等直接设置level属性的logger | For loggers like loguru that set level attribute directly

    @classmethod
    def get_logger(
        cls: Type[T], name: Optional[str] = None, config_name: Optional[str] = None
    ) -> LoggerType:
        """获取日志记录器实例（单例模式）

        单例规则：
        - 相同 (name, config_name) 组合返回同一实例
        - 不同参数组合返回不同实例
        - 全局共享日志配置和级别设置

        Args:
            name (Optional[str]): 日志记录器名称 | Logger name
            config_name (Optional[str]): 日志配置名称，用于区分不同的日志配置 | Log config name for distinguishing different log configurations

        Returns:
            LoggerType: 日志记录器实例 | Logger instance
        """
        # 每次获取logger时都检查verbose参数（支持运行时参数变化）| Check verbose argument each time getting logger (support runtime parameter changes)
        cls._check_verbose_arg()

        # 生成唯一键 | Generate unique key
        key = f"{config_name or 'default'}:{name or 'root'}"

        # 如果已有实例则直接返回 | Return existing instance if available
        if key in cls._loggers:
            return cls._loggers[key]

        # 初始化新实例 | Initialize new instance
        if cls._default_logger is None:
            cls._initialize_logger()

        # 确保default_logger不为None | Ensure default_logger is not None
        assert (
            cls._default_logger is not None
        ), "Default logger should not be None at this point"

        # 如果设置了自定义logger，则直接使用自定义logger
        # If a custom logger is set, use it directly regardless of name/config_name
        if cls._using_custom_logger:
            logger = cls._default_logger
        # 否则根据logger类型获取实例 | Otherwise get instance based on logger type
        elif hasattr(cls._default_logger, "getLogger"):
            # 对于标准库logging等支持getLogger方法的logger | For standard library logging that supports getLogger method
            logger = (
                cls._default_logger.getLogger(name) if name else cls._default_logger
            )
            if hasattr(logger, "set_config_name") and config_name:
                # 对于支持config_name的自定义logger | For custom loggers that support config_name
                logger.set_config_name(config_name)
        else:
            # 对于不支持getLogger的logger（如loguru、print等）| For loggers that don't support getLogger (like loguru, print)
            logger = cls._default_logger

        # 缓存并返回 | Cache and return
        cls._loggers[key] = logger
        return logger

    @classmethod
    def get_default_logger(cls: Type[T]) -> LoggerType:
        """获取全局默认日志记录器实例

        Returns:
            LoggerType: 全局默认日志记录器实例 | Global default logger instance
        """
        if cls._default_logger is None:
            cls._initialize_logger()

        # 确保返回值不为None | Ensure return value is not None
        assert (
            cls._default_logger is not None
        ), "Default logger should not be None after initialization"
        return cls._default_logger


def set_default_logger(logger: LoggerType) -> None:
    """设置全局默认日志记录器 | Set global default logger

    这个函数会将给定的logger设置为全局默认logger，并清除之前的所有缓存实例。
    This function sets the given logger as the global default logger and clears all previously cached instances.

    Args:
        logger (LoggerType): 日志记录器实例 | Logger instance
    """
    LoggerManager._using_custom_logger = (
        True  # 标记使用自定义logger | Mark that a custom logger is being used
    )
    LoggerManager.set_default_logger(logger)


def set_print_mode(enabled: bool) -> None:
    """设置打印模式 | Set print mode

    Args:
        enabled (bool): 是否启用打印模式 | Whether to enable print mode
    """
    LoggerManager.set_print_mode(enabled)


def set_log_level(level: LogLevel) -> None:
    """设置日志级别 | Set log level

    Args:
        level (LogLevel): 日志级别 | Log level
    """
    LoggerManager.set_log_level(level)


def get_logger(
    name: Optional[str] = None, config_name: Optional[str] = None
) -> LoggerType:
    """获取日志记录器 | Get logger

    Args:
        name (Optional[str]): 日志记录器名称 | Logger name
        config_name (Optional[str]): 日志配置名称 | Log config name

    Returns:
        LoggerType: 日志记录器实例 | Logger instance
    """
    return LoggerManager.get_logger(name, config_name)
