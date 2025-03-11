import unittest
from group_center.utils.log.logger import (
    get_logger,
    set_print_mode,
)  # 导入日志模块 / Import logger module
from pathlib import Path  # 导入路径处理模块 / Import path handling module
import os  # 导入操作系统模块 / Import OS module


class TestLogger(unittest.TestCase):
    """
    测试日志模块的单元测试类 | Unit test class for logger module
    """

    def setUp(self) -> None:
        """设置测试前的初始化操作 | Setup method that runs before each test"""
        self.log_dir = Path("test_logs")  # 创建测试日志目录 / Create test log directory
        self.log_dir.mkdir(
            exist_ok=True
        )  # 创建目录，若已存在则不报错 / Create directory if it doesn't exist

    def tearDown(self) -> None:
        """设置测试后的清理操作 | Cleanup method that runs after each test"""
        for f in self.log_dir.glob(
            "*.log"
        ):  # 遍历所有日志文件 / Iterate through all log files
            os.remove(f)  # 删除日志文件 / Remove log file
        self.log_dir.rmdir()  # 删除日志目录 / Remove log directory

    def test_auto_backend(self) -> None:
        """
        测试自动后端切换功能 | Test auto backend switching functionality
        """
        # 测试打印后端 | Test print backend
        # set_print_mode(True)

        # 创建日志配置（未使用）| Create logging config (not used)
        # config = LoggingConfig(log_dir=self.log_dir, config_name="test")
        logger = get_logger()  # 获取默认日志记录器 / Get default logger
        logger.info(
            "This should print to console"
        )  # 记录信息，应打印到控制台 / Log info that should print to console

        # 测试文件后端 | Test file backend
        set_print_mode(False)  # 设置为文件模式 / Set to file mode
        logger = get_logger(
            config_name="auto_test"
        )  # 获取指定配置的日志记录器 / Get logger with specific config
        logger.info(
            "This should write to file"
        )  # 记录信息，应写入文件 / Log info that should write to file

        log_files = list(
            self.log_dir.glob("*.log")
        )  # 获取所有日志文件列表 / Get list of all log files
        print(log_files)  # 打印日志文件列表 / Print log files
        self.assertTrue(
            len(log_files) > 0
        )  # 确保至少有一个日志文件存在 / Assert that there is at least one log file

    def test_config_names(self) -> None:
        """
        测试不同配置名称的日志记录器 | Test different config names for logger
        """
        # 创建两个不同的日志配置（未使用）| Create two different logging configs (not used)
        # config1 = LoggingConfig(log_dir=self.log_dir, config_name="test1")
        # config2 = LoggingConfig(log_dir=self.log_dir, config_name="test2")

        logger1 = get_logger(
            config_name="config1"
        )  # 获取第一个配置的日志记录器 / Get first config's logger
        logger2 = get_logger(
            config_name="config2"
        )  # 获取第二个配置的日志记录器 / Get second config's logger

        logger1.info(
            "This is from config1"
        )  # 记录来自第一个配置的信息 / Log info from first config
        logger2.info(
            "This is from config2"
        )  # 记录来自第二个配置的信息 / Log info from second config

        log_files = list(
            self.log_dir.glob("*.log")
        )  # 获取所有日志文件列表 / Get list of all log files
        print(log_files)  # 打印日志文件列表 / Print log files
        self.assertEqual(
            len(log_files), 2
        )  # 确保有两个不同的日志文件 / Assert that there are two different log files


if __name__ == "__main__":
    unittest.main()  # 运行单元测试主程序 | Run unit test main program
