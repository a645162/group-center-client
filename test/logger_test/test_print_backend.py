import unittest
from io import StringIO
import sys
from group_center.utils.log.backend_print import get_print_backend


class TestPrintBackend(unittest.TestCase):
    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_basic_logging(self):
        logger = get_print_backend()

        logger.debug("This is a debug message")
        logger.info("This is an info message")
        logger.warning("This is a warning message")
        logger.error("This is an error message")
        logger.critical("This is a critical message")
        logger.success("This is a success message")

        output = self.held_output.getvalue()

        print(output)

        self.assertIn("This is an info message", output)
        self.assertIn("This is a warning message", output)
        self.assertIn("This is an error message", output)
        self.assertIn("This is a critical message", output)


if __name__ == "__main__":
    unittest.main()
