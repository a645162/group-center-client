from loguru import logger as loguru_logger
from logging import Logger as StdlibLogger
from group_center.utils.log import (
    LogLevel,
    get_logger,
    set_default_logger,
    set_log_level,
)


def test_set_custom_logger():
    # 测试设置自定义logger
    custom_logger = loguru_logger
    set_default_logger(custom_logger)

    # 获取默认logger
    default_logger = get_logger()
    assert default_logger is custom_logger

    # 测试带配置名称的logger
    config_logger = get_logger(config_name="test_config")
    assert config_logger is custom_logger


def test_set_stdlib_logger():
    # 测试设置标准库logger
    std_logger = StdlibLogger("test")
    set_default_logger(std_logger)

    # 验证获取的logger实例
    assert get_logger() is std_logger
    assert get_logger(name="child") is std_logger


def test_log_level_propagation():
    # 测试日志级别设置
    test_logger = loguru_logger
    set_default_logger(test_logger)
    set_log_level(LogLevel.DEBUG)

    # 验证日志级别
    assert test_logger.level == "DEBUG"

    # 切换回标准日志级别
    set_log_level(LogLevel.INFO)
    assert test_logger.level == "INFO"


def test_logger_with_config_name():
    # 测试不同配置名称的logger隔离
    logger1 = get_logger(config_name="config1")
    logger2 = get_logger(config_name="config2")

    # 修改日志级别
    set_log_level(LogLevel.WARNING)

    # 验证配置隔离
    assert logger1.level == "WARNING"
    assert logger2.level == "WARNING"

    # 测试设置不同的logger后对不同配置的影响
    custom_logger = loguru_logger
    set_default_logger(custom_logger)

    new_logger1 = get_logger(config_name="config1")
    new_logger2 = get_logger(config_name="config2")

    # 验证新logger已正确应用到所有配置
    assert new_logger1 is custom_logger
    assert new_logger2 is custom_logger


def test_clear_cached_loggers():
    # 测试替换logger后缓存清除
    original_logger = get_logger()
    new_logger = loguru_logger
    set_default_logger(new_logger)
    
    # Test Logger
    original_logger.info("This is the original logger")
    new_logger.info("This is the new logger")

    # 验证缓存更新
    assert get_logger() is new_logger
    assert get_logger(config_name="test") is new_logger

    # 再次切换回另一个logger
    std_logger = StdlibLogger("test_again")
    set_default_logger(std_logger)

    # 验证缓存已再次更新
    assert get_logger() is std_logger
    assert get_logger(config_name="test") is std_logger


def test_set_default_logger_with_level():
    """测试设置默认logger后日志级别的正确应用"""
    # 设置初始日志级别
    set_log_level(LogLevel.DEBUG)

    # 设置新的logger
    custom_logger = loguru_logger
    set_default_logger(custom_logger)

    # 验证新logger已正确应用日志级别
    assert get_logger().level == "DEBUG"

    # 修改日志级别并验证
    set_log_level(LogLevel.ERROR)
    assert get_logger().level == "ERROR"


def test_set_default_logger_multiple_times():
    """测试多次切换默认logger的情况"""
    # 初始logger
    logger1 = loguru_logger
    set_default_logger(logger1)
    assert get_logger() is logger1

    # 第二次切换
    logger2 = StdlibLogger("second")
    set_default_logger(logger2)
    assert get_logger() is logger2

    # 第三次切换回原来的logger
    set_default_logger(logger1)
    assert get_logger() is logger1

    # 验证不同名称和配置的logger都已更新
    assert get_logger(name="child") is logger1
    assert get_logger(config_name="other") is logger1


def test_set_default_logger_with_named_loggers():
    """测试设置默认logger后对命名logger的影响"""
    # 创建多个命名logger
    root_logger = get_logger()
    named_logger = get_logger(name="service")
    config_logger = get_logger(config_name="module")
    both_logger = get_logger(name="component", config_name="special")

    # Use
    root_logger.info("Root logger")
    named_logger.info("Named logger")
    config_logger.info("Config logger")
    both_logger.info("Both named and config logger")

    # 设置新的默认logger
    new_logger = loguru_logger
    set_default_logger(new_logger)

    # 验证所有logger都已更新
    assert get_logger() is new_logger
    assert get_logger(name="service") is new_logger
    assert get_logger(config_name="module") is new_logger
    assert get_logger(name="component", config_name="special") is new_logger
