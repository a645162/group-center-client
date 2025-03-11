import unittest
from group_center.utils.log.backend_logging import get_logging_backend, LoggingConfig
from pathlib import Path
import os


class TestLoggingBackend(unittest.TestCase):
    """
    测试日志记录后端的单元测试类 | Unit test class for logging backend
    """

    def setUp(self) -> None:
        """设置测试前的初始化操作 | Setup method that runs before each test"""
        self.log_dir = Path("test_logs")
        self.log_dir.mkdir(exist_ok=True)

    def tearDown(self) -> None:
        """设置测试后的清理操作 | Cleanup method that runs after each test"""
        for f in self.log_dir.glob("*.log"):
            os.remove(f)
        self.log_dir.rmdir()

    def test_basic_logging(self) -> None:
        """
        测试基本的日志记录功能 | Test basic logging functionality
        """
        config = LoggingConfig(log_dir=self.log_dir, config_name="test1")
        logger = get_logging_backend(config)

        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        logger.success("This is a success message")

        log_file = list(self.log_dir.glob("*.log"))[0]
        print(log_file)
        self.assertTrue(log_file.exists())

    def test_multiple_configs(self) -> None:
        """
        测试多个配置的日志记录器 | Test multiple config loggers
        """
        config1 = LoggingConfig(log_dir=self.log_dir, config_name="config1")
        config2 = LoggingConfig(log_dir=self.log_dir, config_name="config2")

        logger1 = get_logging_backend(config1)
        logger2 = get_logging_backend(config2)

        logger1.info("This is from config1")
        logger2.info("This is from config2")

        log_files = list(self.log_dir.glob("*.log"))
        print(log_files)
        self.assertEqual(len(log_files), 2)


if __name__ == "__main__":
    unittest.main()
