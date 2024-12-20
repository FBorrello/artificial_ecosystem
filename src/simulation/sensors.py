# sensors.py

class Sensor:
    """
    Base class for a sensor in the ecosystem simulation. Sensors are used to measure
    various environmental factors or biological metrics within the ecosystem.

    Attributes:
        sensor_id (str): Unique identifier for the sensor.
        location (tuple): Coordinates or position of the sensor in the ecosystem.
        data (dict): Current readings from the sensor.
    """

    def __init__(self, sensor_id, location):
        self.sensor_id = sensor_id
        self.location = location
        self.data = {}

    def measure(self):
        """Abstract method that should be implemented by subclasses to perform measurement."""
        raise NotImplementedError("Subclasses must implement the measure method.")

    def update_data(self, key, value):
        """Update the sensor's data with a new measurement.

        Args:
            key (str): The type of measurement or parameter.
            value (float): The value of the measurement.
        """
        self.data[key] = value

    def get_data(self):
        """
        Retrieve the current data from the sensor.

        Returns:
            dict: The sensor's data dictionary.
        """
        return self.data

    def reset_data(self):
        """Clear the sensor's data store."""
        self.data.clear()


class TemperatureSensor(Sensor):
    def __init__(self, sensor_id, location, precision):
        """
        Initialize a TemperatureSensor with specific attributes.

        :param sensor_id: Unique identifier for the sensor
        :param location: The location where the sensor is installed
        :param precision: The metrological precision of the sensor
        """
        super().__init__(sensor_id, location)
        self.sensor_id = sensor_id
        self.location = location
        self.precision = precision
        self.temperature = 0.0  # Default temperature value

    def read_temperature(self):
        """
        Simulate reading a temperature. In a real scenario, this would interface with hardware.
        """
        # This is a placeholder for actual temperature reading logic
        import random
        self.temperature = random.uniform(20.0, 30.0)
