from typing import Optional
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from group_center.utils.log.log_level import LogLevel

# from group_center.utils.log import new_logging
from group_center.utils.envs import get_a_tmp_dir

# 注册SUCCESS日志级别
logging.addLevelName(LogLevel.SUCCESS.value, "SUCCESS")
logging.SUCCESS = LogLevel.SUCCESS.value  # 设置logging模块的SUCCESS常量


class LoggingConfig:
    """日志配置类"""

    def __init__(
        self,
        level: LogLevel = LogLevel.DEBUG,
        format_str: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        date_format: str = "%Y-%m-%d %H:%M:%S",
        max_file_size: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        log_dir: Optional[Path] = None,
        config_name: Optional[str] = None,
    ):
        self.level = level
        self.format_str = format_str
        self.date_format = date_format
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        self.log_dir = log_dir or get_a_tmp_dir()
        self.config_name = config_name


def _setup_logging(config: Optional[LoggingConfig] = None) -> None:
    """初始化日志配置

    Args:
        config: 日志配置对象
    """
    if config is None:
        config = LoggingConfig()

    # 关闭并清除现有处理器
    logger = logging.getLogger()
    for handler in logger.handlers:
        try:
            handler.close()
        except Exception:
            pass
    logger.handlers.clear()

    # 创建格式化器
    formatter = logging.Formatter(fmt=config.format_str, datefmt=config.date_format)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(config.level.value)

    # 文件处理器
    from datetime import datetime

    log_file_name = f"group_center_{config.config_name or 'default'}_{datetime.now().strftime('%Y-%m-%d')}.log"
    log_file = config.log_dir / log_file_name
    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=config.max_file_size,
        backupCount=config.backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(config.level.value)

    # 配置根日志记录器
    logger = logging.getLogger()
    logger.setLevel(config.level.value)
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # 添加SUCCESS方法到Logger类
    def success(self, msg, *args, **kwargs):
        if self.isEnabledFor(LogLevel.SUCCESS.value):
            self._log(LogLevel.SUCCESS.value, msg, args, **kwargs)

    logging.Logger.success = success


def get_logging_backend(config: Optional[LoggingConfig] = None) -> logging.Logger:
    """获取日志记录器

    Args:
        config: 日志配置对象

    Returns:
        logging.Logger: 配置好的日志记录器
    """
    _setup_logging(config)
    return logging.getLogger("group_center")
