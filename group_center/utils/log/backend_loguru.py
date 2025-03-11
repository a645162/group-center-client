from typing import Optional
from pathlib import Path
from datetime import timedelta
import loguru
from loguru import logger

from group_center.utils.log.log_level import LogLevel, LogLevelManager
from group_center.utils.envs import get_a_tmp_dir


class LoguruConfig:
    """Loguru 日志配置类
    Loguru logging configuration class"""

    def __init__(
        self,
        log_dir: Optional[Path] = None,
        retention: timedelta = timedelta(days=30),
        rotation: str = "10 MB",
        compression: Optional[str] = "zip",
        format_str: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>",
        config_name: Optional[str] = None,
    ):
        """初始化 Loguru 配置
        Initialize Loguru configuration

        Args:
            log_dir: 日志目录 / Log directory
            retention: 日志保留时间 / Log retention period
            rotation: 日志轮转条件 / Log rotation condition
            compression: 日志压缩格式 / Log compression format
            format_str: 日志格式 / Log format
            config_name: 配置名称 / Configuration name
        """
        self.log_dir = log_dir or get_a_tmp_dir()
        self.retention = retention
        self.rotation = rotation
        self.compression = compression
        self.format_str = format_str
        self.config_name = config_name


def _configure_loguru(config: Optional[LoguruConfig] = None) -> None:
    """配置 Loguru 日志记录器
    Configure Loguru logger

    Args:
        config: Loguru 配置对象 / Loguru configuration object
    """
    if config is None:
        config = LoguruConfig()

    # 确保日志目录存在
    config.log_dir.mkdir(parents=True, exist_ok=True)

    # 清除现有处理器
    logger.remove()

    # 添加文件处理器
    from datetime import datetime

    log_file_name = f"group_center_{config.config_name or 'default'}_{datetime.now().strftime('%Y-%m-%d')}.log"
    log_file = config.log_dir / log_file_name

    log_level: LogLevel = LogLevelManager.get_level()
    loguru_level_str: str = str(log_level.name).upper()

    logger.add(
        sink=log_file,
        retention=config.retention,
        rotation=config.rotation,
        compression=config.compression,
        format=config.format_str,
        level=loguru_level_str,
    )

    # 添加控制台处理器
    logger.add(
        sink=lambda msg: print(msg, end=""),
        format=config.format_str,
        level=loguru_level_str,
    )


def get_loguru_backend(config: Optional[LoguruConfig] = None) -> loguru.logger:  # type: ignore
    """获取配置好的 Loguru 日志记录器
    Get configured Loguru logger

    Args:
        config: Loguru 配置对象 / Loguru configuration object

    Returns:
        loguru.Logger: 配置好的日志记录器 / Configured Loguru logger
    """
    _configure_loguru(config)
    return logger
