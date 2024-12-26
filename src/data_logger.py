# src/data_logger.py

from datetime import datetime
import os
import threading
import time
from functools import wraps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def data_logger_class_decorator_factory(sample_rate: int, log_path: str):
    """
    Create a class decorator for logging class properties at a specified sample rate to a CSV file.

    Args:
        sample_rate (int): The interval in seconds at which class properties are logged.
        log_path (str): The directory path where the log file will be stored.

    Returns:
        function: A decorator function that wraps the target class to enable property logging.

    The decorator logs changes in class properties to a CSV file, with each entry containing a timestamp,
    property name, and property value. The log file is created in the specified directory with a naming
    convention based on the current date and time and the class name.
    """
    def data_logger_class_decorator(cls):
        """


        This decorator wraps a class to monitor its properties and log any changes to a CSV file at a specified
        sample rate. It creates a separate logging thread to handle the periodic logging without blocking
        the main thread.

        Returns:
            Wrapper: A new class that extends the original class with logging capabilities.

        Raises:
            AttributeError: If there is an error accessing a property of the class.

        Example:
            @data_logger_class_decorator
            class MyClass:
                ...
        """
        def get_class_properties():
            """
            Retrieve all property attributes of a class.

            Returns:
                list: A list of property names defined in the class.

            """
            # Get all attributes of the class
            attributes = dir(cls)
            # Filter out only the properties
            properties = [attr for attr in attributes if isinstance(getattr(cls, attr), property)]
            return properties

        def create_log_file():
            """
            Create a log file with a timestamped filename and write the header.

            Returns:
                str: The path to the created log file.

            The log file is named using the current date and time, along with the class name, and is saved in
            the specified log directory. The file is initialized with a header row
            containing 'timestamp', 'property', and 'value'.
            """
            # Create log file with the specified naming convention
            start_log_date = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            log_filename = f"{start_log_date}_{cls.__name__}_log.csv"
            log_file_path = os.path.join(log_path, log_filename)

            # Ensure the log directory exists
            os.makedirs(log_path, exist_ok=True)

            # Open the log file and write the header
            with open(log_file_path, 'w') as log_file:
                log_file.write("timestamp,property,value\n")

            return log_file_path

        class_properties = get_class_properties()

        class Wrapper(cls):
            """
            A wrapper class that logs changes to specified class properties periodically.
            """
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.sample_rate = sample_rate
                self._stop_thread = threading.Event()

                # Create the log file
                self.log_file_path = create_log_file()

                # Initialize a cache for property values
                self._property_cache = {prop: None for prop in class_properties}

                # Start the logging thread
                self._thread = threading.Thread(target=self._log_properties_periodically)
                self._thread.daemon = True
                self._thread.start()

                # Add a delay to allow the log file to be updated after starting the log thread
                time.sleep(2)

            def _log_properties_periodically(self):
                """
                Periodically log sampled attributes until the stop signal is set.

                This method runs in a loop, logging the sampled attributes at intervals defined by `sample_rate`.
                The loop continues until the `_stop_thread` event is set.

                Note:
                    This is a private method intended for internal use only.
                """
                while not self._stop_thread.is_set():
                    self.log_sampled_attributes()
                    time.sleep(self.sample_rate)

            def log_sampled_attributes(self):
                """
                Log changes in sampled attributes to a file.

                This method logs the current values of specified class properties to a log file if they differ
                from previously cached values. It updates the cache with the new values after logging.

                Attributes are only logged if they are not callable and if their current value differs from the
                cached value.

                Errors encountered while accessing attributes are logged as errors.

                The log entries include a timestamp, the property name, and its current value.

                This method checks each property in `class_properties` and logs its value if it has changed since
                the last check. If the log file is not found, the logging thread is stopped.

                Raises:
                    AttributeError: If an attribute cannot be accessed or does not have a valid value.
                    FileNotFoundError: If the log file is not found.
                    Exception: For any unexpected errors during file operations.
                """
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                try:
                    with open(self.log_file_path, 'a') as log_file:
                        for prop in class_properties:
                            try:
                                value = getattr(self, prop)
                                if hasattr(value, '__call__'):
                                    continue
                                # Check if the current value differs from the cached value
                                if self._property_cache[prop] != value:
                                    log_file.write(f"{timestamp},{prop},{value}\n")
                                    self._property_cache[prop] = value  # Update the cache
                            except AttributeError as e:
                                logging.error(f"Error accessing attribute '{prop}' "
                                              f"on instance of class '{cls.__name__}': {e}")
                except FileNotFoundError:
                    self._stop_thread.set()
                    logging.info(f"Log file not found: {self.log_file_path} thread is stopped...")

                except PermissionError:
                    logging.error(f"Permission denied when writing to {self.log_file_path}")
                    # Optionally, you might decide to stop logging or try again after some time
                    self._stop_thread.set()
                    logging.info("Logging stopped due to permission issues.")

                except IOError as e:
                    # This catches other IO-related exceptions not covered by FileNotFoundError or PermissionError
                    logging.error(f"An IOError occurred while writing to the log file: {e}")
                    # Here you might want to decide whether to retry or stop logging
                    if e.errno == 28:  # No space left on device
                        logging.warning("Disk full, stopping logging operations.")
                        self._stop_thread.set()
                    else:
                        logging.info(f"Retrying IO operation in 5 seconds...")
                        time.sleep(5)  # Wait for 5 seconds before retrying or stopping

                except Exception as e:
                    logging.error(f"An unexpected error occurred while writing to the log file: {e}")

            def __getattribute__(self, name):
                # Exclude specific methods from logging
                if name in {'_log_properties_periodically', 'log_sampled_attributes'}:
                    return super().__getattribute__(name)

                # Get the attribute from the current class
                attr = super().__getattribute__(name)
                # Check if the attribute is a method of the Wrapper class
                if callable(attr):
                    @wraps(attr)
                    def new_func(*args, **kwargs):
                        logging.info(f"Calling method: {name} with args: {args}, kwargs: {kwargs}")
                        result = attr(*args, **kwargs)
                        logging.info(f"Method {name} returned: {result}")
                        return result

                    return new_func
                return attr

            def __del__(self):
                # Stop the logging thread when the instance is destroyed
                self._stop_thread.set()

        return Wrapper
    return data_logger_class_decorator
