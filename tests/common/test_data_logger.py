# tests/test_data_logger.py

import os
import unittest
import tempfile
import time
from src.common.data_logger import data_logger_class_decorator_factory

class MockClass:
    def __init__(self, value):
        self._value = value

    @property
    def value(self):
        return self._value

    def increment(self, amount):
        self._value += amount
        return self._value

class TestDataLogger(unittest.TestCase):
    """
    Test case class for testing the DataLogger functionality with a mock class.

    This class uses a temporary directory to store log files and tests various aspects of the logging
    functionality, including initialization, method logging, log file creation, and log file content.

    Methods:
    --------
    setUp():
        Sets up the test environment by creating a temporary directory and decorating a mock class.
    tearDown():
        Cleans up the test environment by deleting the temporary directory and its contents.
    test_initialization():
        Tests the initialization of the decorated class instance.
    test_method_logging():
        Tests that method calls are logged correctly.
    test_log_file_creation():
        Tests that a log file is created in the temporary directory.
    test_log_file_contains_correct_data():
        Tests that the log file contains the correct data.
    """
    def setUp(self):
        # Create a temporary directory for logs
        self.temp_dir = tempfile.mkdtemp()

        # Decorate the class with the temporary log path
        self.decorated_class = data_logger_class_decorator_factory(1, self.temp_dir)(MockClass)
        self.instance = self.decorated_class(5)

    def tearDown(self):
        # Stop the logging thread and clean up
        if hasattr(self, 'instance'):
            del self.instance
        # Remove the temporary directory and its contents
        for root, dirs, files in os.walk(self.temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.temp_dir)

    def test_initialization(self):
        """
        Test the initialization of the instance attributes.

        Asserts that the sample_rate and value attributes of the instance are initialized correctly.

        """
        self.assertEqual(self.instance.sample_rate, 1)
        self.assertEqual(self.instance.value, 5)

    def test_method_logging(self):
        """
        Test the logging functionality of the increment method.

        This test checks that the increment method logs the correct information at the INFO level when called
        with specific arguments.

        It verifies that the method logs the input arguments and the return value correctly.

        """
        with self.assertLogs(level='INFO') as log:
            result = self.instance.increment(10)
            self.assertEqual(result, 15)
            # Allow some time for the log to be captured
            time.sleep(0.1)
            self.assertIn('Calling method: increment with args: (10,), kwargs: {}', log.output[0])
            self.assertIn('Method increment returned: 15', log.output[1])

    def test_log_file_creation(self):
        """
        Test if a log file is created in the temporary directory.

        Asserts that there is at least one file in the temporary directory with a name ending
        in '_MockClass_log.csv'.
        """
        # Check if a log file is created in the temporary directory
        log_files = os.listdir(self.temp_dir)
        self.assertTrue(any(log_file.endswith('_MockClass_log.csv') for log_file in log_files))

    def test_log_file_contains_correct_data(self):
        """
        Test that the log file contains the correct data.

        This method checks for the existence of a log file with a specific naming pattern in the
        temporary directory.
        It verifies that the log file has the correct header and contains expected data entries.

        Raises:
            AssertionError: If no log file is found, if the header is incorrect, or if the expected
            data is not present.
        """
        # Find the log file
        log_files = [f for f in os.listdir(self.temp_dir) if f.endswith('_MockClass_log.csv')]
        self.assertTrue(log_files, "No log file found.")
        log_file_path = os.path.join(self.temp_dir, log_files[0])

        # Read the log file and verify its contents
        with open(log_file_path, 'r') as log_file:
            lines = log_file.readlines()

        # Check that the header is correct
        self.assertEqual(lines[0].strip(), "timestamp,property,value")

        # Check that the logged data is correct
        # Assuming the property 'value' is logged
        self.assertTrue(any("value,5" in line for line in lines[1:]), "Log file does not contain expected data.")


if __name__ == '__main__':
    unittest.main()
