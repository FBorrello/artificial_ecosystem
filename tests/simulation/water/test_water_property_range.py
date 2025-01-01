import unittest
from src.simulation.water.water_property_range import WaterPropertyRange


class TestWaterPropertyRange(unittest.TestCase):
    """
    Unit tests for the WaterPropertyRange class, ensuring correct initialization and validation of property ranges.
    """
    def setUp(self):
        self.properties_ranges = WaterPropertyRange.properties_ranges

    def test_init_property_range(self):
        """
        Test the initialization of the WaterPropertyRange object for temperature property.

            This test checks if the WaterPropertyRange object is correctly initialized with the property name 'temperature',
            lower bound 0.0, and upper bound 100.0. It also verifies the string representation of the object.

            Asserts:
                - The property name is 'temperature'.
                - The lower bound is 0.0.
                - The upper bound is 100.0.
                - The string representation matches the expected format.
        """
        temperature_range = WaterPropertyRange("temperature", 0.0, 100.0)
        self.assertEqual(temperature_range.property_name, "temperature")
        self.assertEqual(temperature_range.lower_bound, 0)
        self.assertEqual(temperature_range.upper_bound, 100)
        self.assertEqual(repr(temperature_range), "Temperature_range(lower=0.0, upper=100.0)")

    def test_property_range_valid_names(self):
        """
        Test that WaterPropertyRange objects are initialized with valid property names.

        Iterates over a list of property names and checks if each name is correctly assigned to the property_name
        attribute of a WaterPropertyRange object.

        Raises:
            AssertionError: If the property_name attribute does not match the expected name.
        """
        for name in self.properties_ranges:
            with self.subTest(name=name):
                range_obj = WaterPropertyRange(name, 1, 1.5)
                self.assertEqual(range_obj.property_name, name)

    def test_property_range_invalid_lower_bound(self):
        """
        Test that WaterPropertyRange raises a ValueError for an invalid lower bound.
        """
        with self.assertRaises(ValueError):
            WaterPropertyRange("temperature", -10, -100)

    def test_property_range_invalid_upper_bound(self):
        """
        Test that WaterPropertyRange raises a ValueError when the upper bound is less than the lower bound.
        """
        with self.assertRaises(ValueError):
            WaterPropertyRange("ph", 100, 90)

    def test_property_range_invalid_name(self):
        """
        Test that WaterPropertyRange raises a TypeError for an invalid property name.
        """
        with self.assertRaises(TypeError):
            WaterPropertyRange(100, "turbidity", 100)

    def test_property_range_invalid_empty_string_name(self):
        """
        Test that WaterPropertyRange raises a ValueError when initialized with an empty string as the name.
        """
        with self.assertRaises(ValueError):
            WaterPropertyRange('', 10, 100)

    def test_property_range_invalid_whitespace_name(self):
        """
        Test that WaterPropertyRange raises a ValueError for a name with only whitespace.
        """
        with self.assertRaises(ValueError):
            WaterPropertyRange(' ', 10, 100)

    def test_property_range_invalid_none_name(self):
        """
        Test that WaterPropertyRange raises a TypeError when name is None.

            This test ensures that passing None as the name parameter to the WaterPropertyRange
            constructor raises a TypeError, indicating that the name cannot be None.

        """
        with self.assertRaises(TypeError):
            WaterPropertyRange(None, 10, 100)
