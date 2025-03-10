import unittest
from group_center.utils.log.logger import get_logger, set_print_mode
from pathlib import Path
import os


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.log_dir = Path("test_logs")
        self.log_dir.mkdir(exist_ok=True)

    def tearDown(self):
        for f in self.log_dir.glob("*.log"):
            os.remove(f)
        self.log_dir.rmdir()

    def test_auto_backend(self):
        # Test print backend
        # set_print_mode(True)

        # config = LoggingConfig(log_dir=self.log_dir, config_name="test")
        logger = get_logger()
        logger.info("This should print to console")

        # Test file backend
        set_print_mode(False)
        logger = get_logger(config_name="auto_test")
        logger.info("This should write to file")

        log_files = list(self.log_dir.glob("*.log"))
        print(log_files)
        self.assertTrue(len(log_files) > 0)

    def test_config_names(self):
        # config1 = LoggingConfig(log_dir=self.log_dir, config_name="test1")
        # config2 = LoggingConfig(log_dir=self.log_dir, config_name="test2")

        logger1 = get_logger(config_name="config1")
        logger2 = get_logger(config_name="config2")

        logger1.info("This is from config1")
        logger2.info("This is from config2")

        log_files = list(self.log_dir.glob("*.log"))
        print(log_files)
        self.assertEqual(len(log_files), 2)


if __name__ == "__main__":
    unittest.main()
