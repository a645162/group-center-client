import unittest
from io import StringIO
import sys
from group_center.utils.log.backend_print import get_print_backend


class TestPrintBackend(unittest.TestCase):
    """
    测试打印后端的单元测试类 | Unit test class for print backend
    """

    def setUp(self) -> None:
        """设置测试前的初始化操作 | Setup method that runs before each test"""
        self.held_output: StringIO = StringIO()
        sys.stdout = self.held_output

    def tearDown(self) -> None:
        """设置测试后的清理操作 | Cleanup method that runs after each test"""
        sys.stdout = sys.__stdout__

    def test_basic_logging(self) -> None:
        """
        测试基本的日志记录功能 | Test basic logging functionality
        """
        logger = get_print_backend()

        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        logger.success("This is a success message")

        output: str = self.held_output.getvalue()

        print(output)

        self.assertIn("This is an info message", output)
        self.assertIn("This is a warning message", output)
        self.assertIn("This is an error message", output)
        self.assertIn("This is a critical message", output)


if __name__ == "__main__":
    unittest.main()
