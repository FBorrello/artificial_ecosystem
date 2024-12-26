# `data_logger.py` Module Documentation

## Overview
The `data_logger.py` module is designed to enable systematic logging of class property changes and method calls, providing insights into object behavior over time. By leveraging decorators, users can easily integrate logging functionality into their classes. This module is particularly useful for debugging, monitoring, and analyzing the runtime state of objects. The logged data is stored in structured log files for later examination.

---

## Features
1. **Class Level Logging with Decorators**: Automatically logs changes to properties and method calls for decorated classes.
2. **Customizable Log File Storage**: Specify custom log file locations for easy file management.
3. **Structured Log Output**: Logs are stored in organized CSV files for accessibility and easy analysis.
4. **Thread-safe Logging**: Ensures logs are created and updated in a thread-safe manner.

---

## Core Components

### 1. **`data_logger_class_decorator_factory(sample_rate: int, log_dir: str)`**
This is the main factory function responsible for generating a decorator for logging classes. It wraps a class to automatically log property values and method calls.

**Parameters:**
- `sample_rate` _(int)_: Determines how frequently the logging system monitors property changes (in seconds).
- `log_dir` _(str)_: Path to the directory where the log files will be created and stored.

**Returns:**
- A class decorator that augments the functionality of the targeted class.

---

## Log Structure
The log files created by the module follow a specific structure to ensure clarity and ease of use. Files are saved in CSV format with the following structure:

### Headers:
- **`timestamp`**: The time (in ISO-8601 format) when the log entry was written.
- **`property`**: The name of the property being logged.
- **`value`**: The value of the property at the time of logging.

### Example Log Entry:

```csv file
timestamp,property,value 
2023-10-12T15:30:45,value,5 
2023-10-12T15:31:46,value,10
```


---

## Usage

### 1. **Decorating a Class**

Use `data_logger_class_decorator_factory` to decorate the required class and augment its functionality with logging.

```python
from data_logger import data_logger_class_decorator_factory

# Create a decorator with a sample rate of 1 second and a log directory
logger_decorator = data_logger_class_decorator_factory(sample_rate=1, log_dir="path/to/logs")

@logger_decorator
class MyClass:
    def __init__(self, value):
        self.value = value

    def increment(self, amount):
        self.value += amount
        return self.value
```

In this example:
- The class `MyClass` is decorated to log changes to its `value` property and method calls like `increment()`.

---

### 2. **Log File Creation**
The log file is named using the naming convention: `<CLASS_NAME>_log.csv`. For instance, for `MyClass`, the log file will be named `MyClass_log.csv`.

Logs are automatically written to the directory specified in `log_dir` during decorator initialization.

---

## Best Practices
1. **Choose an Appropriate Sample Rate:**
   - The `sample_rate` should be chosen based on how frequently changes are expected in properties.
   - A lower sample rate (e.g. 1 second) is good for rapid updates, while a higher one (e.g. 10 seconds) can decrease resource usage for less active applications.

2. **File Management:**
   - Periodically archive or delete old log files to manage disk space effectively.

3. **Custom Log Directory:**
   - Always provide a fixed path for `log_dir` to ensure logs are stored in a predictable location.

---

## Testing
Tests for this module are implemented to ensure its correctness and reliability. Below is an overview of the testing scenarios covered in `test_data_logger.py`:

1. **Initialization**: Verifies that the decorated class has the correct `sample_rate` and initial property values.
2. **Logged Method Calls**: Ensures that calls to decorated methods are correctly logged, including arguments and return values.
3. **Log File Creation**: Checks that the module creates appropriate log files in the specified directory.
4. **Log File Content**: Confirms that the log files are populated with correct information including headers and entries.

Testing is done using the `unittest` library. Temporary directories and files are created for testing and then cleaned up to avoid side effects.

---

## Limitations
1. **Assumes CSV Header Stability**: The expected log file will always have the same header format.
2. **File I/O Overhead**: Logging introduces file I/O overhead, especially with low `sample_rate` values; consider this for latency-critical systems.
3. **Thread Safety Assumptions**: While logging is designed to be thread-safe, complex multithreaded applications may need additional verification based on usage.

---

## Conclusion
The `data_logger.py` module provides a robust solution for real-time logging of object state changes and interactions. Its ease of integration, customizable settings, and well-structured outputs make it suitable for a wide range of applications, including debugging, monitoring, and analytics. Use the provided decorator factory to quickly add logging functionality to your classes and analyze runtime behaviors effortlessly.