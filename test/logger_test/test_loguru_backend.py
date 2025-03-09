import unittest
from group_center.utils.log.backend_loguru import get_loguru_backend, LoguruConfig
from group_center.utils.log.log_level import LogLevel
from pathlib import Path
import os


class TestLoguruBackend(unittest.TestCase):
    def setUp(self):
        self.log_dir = Path("test_logs")
        self.log_dir.mkdir(exist_ok=True)

    def tearDown(self):
        for f in self.log_dir.glob("*.log"):
            os.remove(f)
        self.log_dir.rmdir()

    def test_basic_logging(self):
        config = LoguruConfig(log_dir=self.log_dir, config_name="test1")
        logger = get_loguru_backend(config)

        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        logger.success("This is a success message")

        log_file = list(self.log_dir.glob("*.log"))[0]
        print(log_file)
        self.assertTrue(log_file.exists())

    def test_multiple_configs(self):
        config1 = LoguruConfig(log_dir=self.log_dir, config_name="config1")
        config2 = LoguruConfig(log_dir=self.log_dir, config_name="config2")

        logger1 = get_loguru_backend(config1)
        logger2 = get_loguru_backend(config2)

        logger1.info("This is from config1")
        logger2.info("This is from config2")

        log_files = list(self.log_dir.glob("*.log"))
        print(log_files)
        self.assertEqual(len(log_files), 2)


if __name__ == "__main__":
    unittest.main()
