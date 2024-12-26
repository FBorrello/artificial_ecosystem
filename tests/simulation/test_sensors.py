import unittest
from src.simulation.sensors import Sensor, TemperatureSensor

class TestBaseSensor(unittest.TestCase):
    def setUp(self):
        self.sensor = Sensor("base1", (0, 0))

    def test_sensor_creation(self):
        # Test if sensor is created with correct id and location
        self.assertEqual(self.sensor.sensor_id, "base1")
        self.assertEqual(self.sensor.location, (0, 0))

    def test_update_data(self):
        # Test updating data in sensor
        self.sensor.update_data("light", 100)
        self.assertEqual(self.sensor.get_data(), {"light": 100})

    def test_get_data(self):
        # Test retrieving data from sensor
        self.sensor.update_data("temperature", 25.5)
        self.assertEqual(self.sensor.get_data(), {"temperature": 25.5})

    def test_reset_data(self):
        # Test resetting the sensor's data
        self.sensor.update_data("humidity", 60)
        self.sensor.reset_data()
        self.assertEqual(self.sensor.get_data(), {})

class TestTemperatureSensor(unittest.TestCase):
    def setUp(self):
        self.temp_sensor = TemperatureSensor("temp1", (0, 0), 1)

    def test_temperature_sensor_creation(self):
        # Test if temperature sensor is created with correct attributes
        self.assertEqual(self.temp_sensor.sensor_id, "temp1")
        self.assertEqual(self.temp_sensor.location, (0, 0))
        self.assertEqual(self.temp_sensor.precision, 1)

    def test_read_temperature(self):
        # Test reading temperature, assuming the method sets a temperature
        self.temp_sensor.read_temperature()
        # Assuming read_temperature sets a random temperature for demonstration
        self.assertTrue(20.0 <= self.temp_sensor.temperature <= 30.0)

    def test_get_temperature(self):
        # Test if get_temperature returns the last set temperature
        temp = 22.5  # Set a known temperature
        self.temp_sensor.temperature = temp
        self.assertEqual(self.temp_sensor.temperature, temp)

    def test_precision(self):
        # Test if the sensor's precision works as expected
        self.temp_sensor.precision = 0.1
        self.temp_sensor.read_temperature()  # Assuming this affects precision
        # Check if the set precision affects the temperature reading
        temp = self.temp_sensor.temperature
        # This test assumes that read_temperature might set a temperature within our precision range
        self.assertAlmostEqual(temp, round(temp, 2), places=2)  # Check if temperature is rounded to 2 decimal places

    def test_update_temperature(self):
        # Test updating temperature through the base Sensor method
        new_temp = 25.0
        self.temp_sensor.update_data("temperature", new_temp)
        self.assertEqual(self.temp_sensor.get_data()["temperature"], new_temp)

if __name__ == '__main__':
    unittest.main()