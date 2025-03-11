import unittest
from group_center.utils.log.backend_loguru import get_loguru_backend, LoguruConfig
from pathlib import Path
import os


class TestLoguruBackend(unittest.TestCase):
    def setUp(self) -> None:
        """Initialize test environment 初始化测试环境"""
        self.log_dir = Path("test_logs")  # Directory for test logs 测试日志目录
        self.log_dir.mkdir(
            exist_ok=True
        )  # Create directory if not exists 如果目录不存在则创建

    def tearDown(self) -> None:
        """Clean up test environment 清理测试环境"""
        for f in self.log_dir.glob("*.log"):  # Remove all log files 删除所有日志文件
            os.remove(f)
        self.log_dir.rmdir()  # Remove log directory 删除日志目录

    def test_basic_logging(self) -> None:
        """Test basic logging functionality 测试基本日志功能"""
        config = LoguruConfig(
            log_dir=self.log_dir, config_name="test1"
        )  # Create config 创建配置
        logger = get_loguru_backend(config)  # Get logger instance 获取日志实例

        # Test different log levels 测试不同日志级别
        logger.debug("This is a debug message")  # Debug message 调试信息
        logger.info("This is an info message")  # Info message 信息
        logger.warning("This is a warning message")  # Warning message 警告信息
        logger.error("This is an error message")  # Error message 错误信息
        logger.critical("This is a critical message")  # Critical message 严重错误信息
        logger.success("This is a success message")  # Success message 成功信息

        log_file = list(self.log_dir.glob("*.log"))[0]  # Get log file 获取日志文件
        print(log_file)
        self.assertTrue(log_file.exists())  # Verify log file exists 验证日志文件存在

    def test_multiple_configs(self) -> None:
        """Test multiple logger configurations 测试多个日志配置"""
        config1 = LoguruConfig(
            log_dir=self.log_dir, config_name="config1"
        )  # Config 1 配置1
        config2 = LoguruConfig(
            log_dir=self.log_dir, config_name="config2"
        )  # Config 2 配置2

        logger1 = get_loguru_backend(config1)  # Logger instance 1 日志实例1
        logger2 = get_loguru_backend(config2)  # Logger instance 2 日志实例2

        logger1.info(
            "This is from config1"
        )  # Log message from config1 来自config1的日志信息
        logger2.info(
            "This is from config2"
        )  # Log message from config2 来自config2的日志信息

        log_files = list(
            self.log_dir.glob("*.log")
        )  # Get all log files 获取所有日志文件
        print(log_files)
        self.assertEqual(
            len(log_files), 2
        )  # Verify two log files exist 验证存在两个日志文件


if __name__ == "__main__":
    unittest.main()  # Run unit tests 运行单元测试
