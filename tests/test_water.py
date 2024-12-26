# tests/tests_water.py

import unittest
from src.simulation.water import Water, WaterPropertyRange, WaterQualityMonitor

class TestWaterPropertyRange(unittest.TestCase):
    """
    Unit tests for the WaterPropertyRange class, ensuring correct initialization and validation of property ranges.
    """
    properties_ranges = {
        "temperature",
        "ph",
        "turbidity",
        "viscosity",
        "tds"
    }
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

                Iterates over a list of property names and checks if each name is correctly assigned to the property_name attribute of a WaterPropertyRange object.

                Raises:
                    AssertionError: If the property_name attribute does not match the expected name.
        """
        for name in self.properties_ranges:
            with self.subTest(name=name):
                range_obj = WaterPropertyRange(name, 0, 100)
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

class TestWater(unittest.TestCase):

    def test_init(self):
        initial_nutrients = 50
        tank_capacity = 200
        water = Water(initial_nutrients, tank_capacity)

        self.assertEqual(water.nutrients, initial_nutrients)
        self.assertEqual(water.tank_capacity, tank_capacity)
        self.assertEqual(water.current_nutrients, initial_nutrients)
        self.assertEqual(water.current_volume, 0, "Initial current volume should be 0")
        self.assertEqual(water.snow_accumulation, 0, "Initial snow accumulation should be 0")
        self.assertEqual(water.temperature, 25)
        self.assertEqual(water.ph, 7.0)
        self.assertEqual(water.turbidity, 0)
        self.assertEqual(water.viscosity, 1.0)
        self.assertEqual(water.tds, 0)

class TestWaterTemperature(unittest.TestCase):

    def setUp(self):
        """Set up a Water instance for testing."""
        self.water = Water(initial_nutrients=50, tank_capacity=200)

    def test_default_temperature(self):
        """Test the default temperature value."""
        self.assertEqual(self.water.temperature, 25, "Default temperature should be 25°C")

    def test_set_valid_temperature(self):
        """Test setting a valid temperature."""
        valid_temperatures = [-10, 0, 25, 50, 100]
        for temp in valid_temperatures:
            with self.subTest(temp=temp):
                self.water.temperature = temp
                self.assertEqual(self.water.temperature, temp, f"Temperature should be set to {temp}°C")

    def test_set_invalid_temperature(self):
        """Test setting an invalid temperature raises ValueError."""
        invalid_temperatures = [-20, 150]
        for temp in invalid_temperatures:
            with self.subTest(temp=temp):
                with self.assertRaises(ValueError, msg=f"Setting temperature to {temp}°C should raise ValueError"):
                    self.water.temperature = temp

    def test_set_invalid_temperature_type(self):
        """
        Test Scenario: Test the temperature property with an invalid type by attempting to set it to a string value,
        expecting a TypeError to be raised, ensuring type safety and robustness of the temperature setter method.
        """
        with self.assertRaises(TypeError):
            self.water.temperature = "thirty"

    def test_temperature_influence(self):
        """Test if temperature influences other properties or methods (if applicable)."""
        # Placeholder for any additional tests related to temperature's influence
        # For example, if temperature affects viscosity, you would test that here
        pass

class TestWaterPH(unittest.TestCase):

    def setUp(self):
        """Set up a Water instance for testing."""
        self.water = Water(initial_nutrients=50, tank_capacity=200)

    def test_default_ph(self):
        """Test the default pH value."""
        self.assertEqual(self.water.ph, 7.0, "Default pH should be 7.0")

    def test_set_valid_ph(self):
        """Test setting a valid pH."""
        valid_ph_values = [0, 7, 14]
        for ph in valid_ph_values:
            with self.subTest(ph=ph):
                self.water.ph = ph
                self.assertEqual(self.water.ph, ph, f"pH should be set to {ph}")

    def test_set_invalid_ph(self):
        """Test setting an invalid pH raises ValueError."""
        invalid_ph_values = [-1, 15]
        for ph in invalid_ph_values:
            with self.subTest(ph=ph):
                with self.assertRaises(ValueError, msg=f"Setting pH to {ph} should raise ValueError"):
                    self.water.ph = ph

class TestWaterTurbidity(unittest.TestCase):

    def setUp(self):
        """Set up a Water instance for testing."""
        self.water = Water(initial_nutrients=50, tank_capacity=200)

    def test_default_turbidity(self):
        """Test the default turbidity value."""
        self.assertEqual(self.water.turbidity, 0, "Default turbidity should be 0")

    def test_set_valid_turbidity(self):
        """Test setting a valid turbidity."""
        valid_turbidity_values = [0, 5, 10]
        for turbidity in valid_turbidity_values:
            with self.subTest(turbidity=turbidity):
                self.water.turbidity = turbidity
                self.assertEqual(self.water.turbidity, turbidity, f"Turbidity should be set to {turbidity}")

    def test_set_invalid_turbidity(self):
        """Test setting an invalid turbidity raises ValueError."""
        with self.assertRaises(ValueError, msg="Setting turbidity to a negative value should raise ValueError"):
            self.water.turbidity = -1

class TestWaterViscosity(unittest.TestCase):

    def setUp(self):
        """Set up a Water instance for testing."""
        self.water = Water(initial_nutrients=50, tank_capacity=200)

    def test_default_viscosity(self):
        """Test the default viscosity value."""
        self.assertEqual(self.water.viscosity, 1.0, "Default viscosity should be 1.0")

    def test_set_valid_viscosity(self):
        """Test setting a valid viscosity."""
        valid_viscosity_values = [0.1, 1.0, 10.0]
        for viscosity in valid_viscosity_values:
            with self.subTest(viscosity=viscosity):
                self.water.viscosity = viscosity
                self.assertEqual(self.water.viscosity, viscosity, f"Viscosity should be set to {viscosity}")

    def test_set_invalid_viscosity(self):
        """Test setting an invalid viscosity raises ValueError."""
        with self.assertRaises(ValueError, msg="Setting viscosity to a non-positive value should raise ValueError"):
            self.water.viscosity = 0

class TestWaterTDS(unittest.TestCase):

    def setUp(self):
        """Set up a Water instance for testing."""
        self.water = Water(initial_nutrients=50, tank_capacity=200)

    def test_default_tds(self):
        """Test the default TDS value."""
        self.assertEqual(self.water.tds, 0, "Default TDS should be 0")

    def test_set_valid_tds(self):
        """Test setting a valid TDS."""
        valid_tds_values = [0, 50, 100]
        for tds in valid_tds_values:
            with self.subTest(tds=tds):
                self.water.tds = tds
                self.assertEqual(self.water.tds, tds, f"TDS should be set to {tds}")

    def test_set_invalid_tds(self):
        """Test setting an invalid TDS raises ValueError."""
        with self.assertRaises(ValueError, msg="Setting TDS to a negative value should raise ValueError"):
            self.water.tds = -10

class TestWaterPrecipitationManagement(unittest.TestCase):

    def setUp(self):
        """Set up a Water instance for testing."""
        self.water = Water(initial_nutrients=50, tank_capacity=200)

    def test_manage_precipitation_rain(self):
        """Test managing precipitation with rain."""
        precipitation_type = 'rain'
        amount = 20
        pattern = 'steady'

        initial_volume = self.water.current_volume
        self.water.manage_precipitation(precipitation_type, amount, pattern)

        expected_volume = initial_volume + amount
        self.assertEqual(self.water.current_volume, expected_volume,
                         "Water volume should increase by the amount of rain")

    def test_manage_precipitation_snow(self):
        """Test managing precipitation with snow."""
        precipitation_type = 'snow'
        amount = 10
        pattern = 'intermittent'

        # Set temperature to a value above 0 to allow snow melting
        self.water.temperature = 5

        initial_volume = self.water.current_volume
        self.water.manage_precipitation(precipitation_type, amount, pattern)

        # Calculate expected volume after snow melting
        expected_melted_snow = min(amount, self.water.temperature)
        expected_volume = initial_volume + expected_melted_snow

        self.assertEqual(self.water.current_volume, expected_volume,
                         "Water volume should reflect snow accumulation and melting")

    def test_invalid_precipitation_type(self):
        """Test handling of invalid precipitation type."""
        with self.assertRaises(ValueError, msg="Invalid precipitation type should raise ValueError"):
            self.water.manage_precipitation('hail', 10, 'steady')

    def test_precipitation_exceeds_capacity(self):
        """Test precipitation management when it exceeds tank capacity."""
        precipitation_type = 'rain'
        amount = 300  # Exceeds tank capacity
        pattern = 'steady'

        self.water.manage_precipitation(precipitation_type, amount, pattern)

        self.assertEqual(self.water.current_volume, self.water.tank_capacity,
                         "Water volume should not exceed tank capacity")

class TestWaterQualityMonitor(unittest.TestCase):
    """
        Unit tests for the WaterQualityMonitor class.

        This test suite includes tests for initialization, data validation, data analysis, alert generation, and output status of the WaterQualityMonitor class.

        Methods
        -------
        test_water_quality_monitor_init():
            Tests the initialization of the WaterQualityMonitor object.
        test_water_quality_monitor_data_validation():
            Tests the validation of data within acceptable limits.
        test_water_quality_monitor_data_validation_invalid_data_name():
            Tests the validation of data with an invalid parameter name.
        test_water_quality_monitor_data_validation_invalid_data_value():
            Tests the validation of data with an invalid parameter value type.
        test_water_quality_monitor_analyze_data():
            Tests the analysis of data within acceptable limits.
        test_water_quality_monitor_analyze_data_out_of_range():
            Tests the analysis of data with out-of-range values.
        test_water_quality_monitor_generate_alert():
            Tests the generation of alerts for out-of-range values.
        test_water_quality_monitor_output_status():
            Tests the output status of the monitor when data is within range.
        test_water_quality_monitor_output_status_out_of_range():
            Tests the output status of the monitor when data is out of range.
        """
    def test_water_quality_monitor_init(self):
        """
        Test the initialization of the WaterQualityMonitor class.

                Ensures that the WaterQualityMonitor is correctly initialized with the given water property ranges and that initial alerts and status are empty.

                Raises:
                    AssertionError: If any of the initial values do not match the expected values.
        """
        ph_range = WaterPropertyRange("ph", 6.5, 8.5)
        turbidity_range = WaterPropertyRange("turbidity", 0, 10)
        temperature_range = WaterPropertyRange("temperature", 10, 30)
        tds_range = WaterPropertyRange("tds", 50, 200)
        monitor = WaterQualityMonitor(ph_range, turbidity_range, temperature_range, tds_range)
        self.assertEqual(monitor.ph_range, ph_range)
        self.assertEqual(monitor.turbidity_range, turbidity_range)
        self.assertEqual(monitor.temperature_range, temperature_range)
        self.assertEqual(monitor.tds_range, tds_range)
        self.assertEqual(monitor.alerts, [], "No alerts initially")
        self.assertEqual(monitor.output_status(), {}, "No status initially")

    def test_water_quality_monitor_data_validation(self):
        """
        Test the data validation functionality of the WaterQualityMonitor class.

            This test checks if the WaterQualityMonitor correctly validates water quality data against predefined acceptable ranges for pH, turbidity, temperature, and TDS.

            Raises:
                AssertionError: If the data does not validate correctly.

        """
        # Define ranges for each parameter
        ph_range = WaterPropertyRange("ph", 6.5, 8.5)
        turbidity_range = WaterPropertyRange("turbidity", 0, 10)
        temperature_range = WaterPropertyRange("temperature", 10, 30)
        tds_range = WaterPropertyRange("tds", 50, 200)

        # Initialize the monitor with these ranges
        monitor = WaterQualityMonitor(ph_range, turbidity_range, temperature_range, tds_range)
        # Check if data is within acceptable limits
        data = {'ph': 7.5, 'turbidity': 5, 'temperature': 20, 'tds': 100}
        self.assertTrue(monitor.validate_data(data))

    def test_water_quality_monitor_data_validation_invalid_data_name(self):
        """
        Test the water quality monitor's data validation for invalid parameter names.

                This test checks that the WaterQualityMonitor raises an AttributeError when the data dictionary
                contains a parameter name that is not recognized by the monitor.

                Raises:
                    AttributeError: If the data contains an invalid parameter name.

        """
        # Define ranges for each parameter
        ph_range = WaterPropertyRange("ph", 6.5, 8.5)
        turbidity_range = WaterPropertyRange("turbidity", 0, 10)
        temperature_range = WaterPropertyRange("temperature", 10, 30)
        tds_range = WaterPropertyRange("tds", 50, 200)

        # Initialize the monitor with these ranges
        monitor = WaterQualityMonitor(ph_range, turbidity_range, temperature_range, tds_range)
        # Check if data is within acceptable limits
        data = {'invalid_parameter': 7.5, 'turbidity': 5, 'temperature': 20, 'tds': 100}
        with self.assertRaises(AttributeError):
            monitor.validate_data(data)

    def test_water_quality_monitor_data_validation_invalid_data_value(self):
        """
        Test the water quality monitor's data validation for invalid data types.

            This test checks that the WaterQualityMonitor raises a TypeError when the data contains invalid types.
            Specifically, it verifies that a string value for 'ph' instead of a numeric value triggers the exception.

            Raises:
                TypeError: If the data contains invalid types for any parameter.

        """
        # Define ranges for each parameter
        ph_range = WaterPropertyRange("ph", 6.5, 8.5)
        turbidity_range = WaterPropertyRange("turbidity", 0, 10)
        temperature_range = WaterPropertyRange("temperature", 10, 30)
        tds_range = WaterPropertyRange("tds", 50, 200)

        # Initialize the monitor with these ranges
        monitor = WaterQualityMonitor(ph_range, turbidity_range, temperature_range, tds_range)
        # Check if data is within acceptable limits
        data = {'ph': '7.5', 'turbidity': 5, 'temperature': 20, 'tds': 100}
        with self.assertRaises(TypeError):
            monitor.validate_data(data)

    def test_water_quality_monitor_analyze_data(self):
        """
        Test the analyze_data method of the WaterQualityMonitor class.

            This test checks if the WaterQualityMonitor correctly identifies data within acceptable limits for pH, turbidity, temperature, and TDS.

            It initializes the WaterQualityMonitor with predefined ranges for each parameter and verifies that the analyze_data method returns True for data within these ranges.
        """
        # Define ranges for each parameter
        ph_range = WaterPropertyRange("ph", 6.5, 8.5)
        turbidity_range = WaterPropertyRange("turbidity", 0, 10)
        temperature_range = WaterPropertyRange("temperature", 10, 30)
        tds_range = WaterPropertyRange("tds", 50, 200)

        # Initialize the monitor with these ranges
        monitor = WaterQualityMonitor(ph_range, turbidity_range, temperature_range, tds_range)
        # Check if data is within acceptable limits
        data = {'ph': 7.5, 'turbidity': 5, 'temperature': 20, 'tds': 100}
        self.assertTrue(monitor.analyze_data(data))

    def test_water_quality_monitor_analyze_data_out_of_range(self):
        """
        Test the WaterQualityMonitor's analyze_data method for out-of-range values.

            This test checks if the analyze_data method correctly identifies when the water quality data is out of the specified acceptable ranges for each parameter.

            It initializes the WaterQualityMonitor with predefined ranges for pH, turbidity, temperature, and TDS, and then verifies that the method returns False when the temperature is out of range.

        """
        # Define ranges for each parameter
        ph_range = WaterPropertyRange("ph", 6.5, 8.5)
        turbidity_range = WaterPropertyRange("turbidity", 0, 10)
        temperature_range = WaterPropertyRange("temperature", 10, 30)
        tds_range = WaterPropertyRange("tds", 50, 200)

        # Initialize the monitor with these ranges
        monitor = WaterQualityMonitor(ph_range, turbidity_range, temperature_range, tds_range)
        # Check if data is within acceptable limits
        data = {'ph': 7.5, 'turbidity': 5, 'temperature': 120, 'tds': 100}
        self.assertFalse(monitor.analyze_data(data))

    def test_water_quality_monitor_generate_alert(self):
        """
        Test the water quality monitor's ability to generate alerts for out-of-range values.

            This test checks if the WaterQualityMonitor correctly identifies and alerts when a parameter value is outside the specified range.

            It sets up a WaterQualityMonitor with defined ranges for pH, turbidity, temperature, and TDS, then provides data with an out-of-range temperature value to verify that an alert is generated.

            Asserts:
                - Data validation should succeed for the given data.
                - Data analysis should fail due to out-of-range temperature.
                - An alert should be generated for the out-of-range temperature.
                - The alert message should correctly indicate the out-of-range parameter and its value.
        """
        # Define ranges for each parameter
        ph_range = WaterPropertyRange("ph", 6.5, 8.5)
        turbidity_range = WaterPropertyRange("turbidity", 0, 10)
        temperature_range = WaterPropertyRange("temperature", 10, 30)
        tds_range = WaterPropertyRange("tds", 50, 200)
        # Initialize the monitor with these ranges
        monitor = WaterQualityMonitor(ph_range, turbidity_range, temperature_range, tds_range)
        # Generate alert for out-of-range values
        data = {'ph': 7.5, 'turbidity': 5, 'temperature': 120, 'tds': 100}
        self.assertTrue(monitor.validate_data(data), 'Data validation should succeed')
        self.assertFalse(monitor.analyze_data(data), 'Data analyses should fail')
        self.assertTrue(len(monitor.alerts) == 1, 'Monitor water quality monitor is empty')
        alert_message = monitor.alerts[0]
        self.assertEqual(f"Alert! temperature: 120 out of range", alert_message, 'Incorrect alert message')

    def test_water_quality_monitor_clean_alert(self):
        # Define ranges for each parameter
        ph_range = WaterPropertyRange("ph", 6.5, 8.5)
        turbidity_range = WaterPropertyRange("turbidity", 0, 10)
        temperature_range = WaterPropertyRange("temperature", 10, 30)
        tds_range = WaterPropertyRange("tds", 50, 200)
        # Initialize the monitor with these ranges
        monitor = WaterQualityMonitor(ph_range, turbidity_range, temperature_range, tds_range)
        # Generate alert for out-of-range values
        data = {'ph': 7.5, 'turbidity': 5, 'temperature': 120, 'tds': 100}
        self.assertTrue(monitor.validate_data(data), 'Data validation should succeed')
        self.assertFalse(monitor.analyze_data(data), 'Data analyses should fail')
        self.assertTrue(len(monitor.alerts) == 1, 'Monitor water quality monitor is empty')
        alert_message = monitor.alerts[0]
        self.assertEqual(f"Alert! temperature: 120 out of range", alert_message, 'Incorrect alert message')
        monitor.clean_alerts()
        self.assertTrue(len(monitor.alerts) == 0, 'Monitor water quality monitor should be empty')

    def test_water_quality_monitor_output_status(self):
        """
        Test the output status of the water quality monitor.

                This test checks if the water quality monitor correctly validates and analyzes data within specified ranges for pH, turbidity, temperature, and TDS. It ensures that the monitor outputs a status without alerts when data is within acceptable ranges.

                Raises:
                    AssertionError: If any of the assertions fail, indicating a problem with data validation, analysis, or output status.
        """
        # Define ranges for each parameter
        ph_range = WaterPropertyRange("ph", 6.5, 8.5)
        turbidity_range = WaterPropertyRange("turbidity", 0, 10)
        temperature_range = WaterPropertyRange("temperature", 10, 30)
        tds_range = WaterPropertyRange("tds", 50, 200)
        # Initialize the monitor with these ranges
        monitor = WaterQualityMonitor(ph_range, turbidity_range, temperature_range, tds_range)
        data = {'ph': 7.5, 'turbidity': 5, 'temperature': 12, 'tds': 100}
        self.assertTrue(monitor.validate_data(data), 'Data validation should succeed')
        self.assertTrue(monitor.analyze_data(data), 'Data analyses should succeed')
        self.assertTrue(len(monitor.alerts) == 0, 'Monitor water quality monitor should be empty')
        # Output status without alerts
        self.assertTrue(monitor.output_status() != {}, 'Output status should return a not empty dictionary')
        self.assertTrue(all(['OK' in item for item in monitor.output_status().values()]),
                        'Output status value should contain OK for all values')

    def test_water_quality_monitor_output_status_out_of_range(self):
        """
        Test the water quality monitor's output status when data is out of range.

            This test checks if the water quality monitor correctly identifies and handles out-of-range values for various water properties such as pH, turbidity, temperature, and TDS. It ensures that the monitor generates alerts for out-of-range values and that the output status reflects these alerts.

            Raises:
                AssertionError: If the data validation or analysis does not behave as expected, or if the output status does not correctly reflect the alerts.
        """
        # Define ranges for each parameter
        ph_range = WaterPropertyRange("ph", 6.5, 8.5)
        turbidity_range = WaterPropertyRange("turbidity", 0, 10)
        temperature_range = WaterPropertyRange("temperature", 10, 30)
        tds_range = WaterPropertyRange("tds", 50, 200)
        # Initialize the monitor with these ranges
        monitor = WaterQualityMonitor(ph_range, turbidity_range, temperature_range, tds_range)
        # Generate alert for out-of-range values
        data = {'ph': 7.5, 'turbidity': 5, 'temperature': 120, 'tds': 100}
        self.assertTrue(monitor.validate_data(data), 'Data validation should succeed')
        self.assertFalse(monitor.analyze_data(data), 'Data analyses should fail')
        self.assertTrue(len(monitor.alerts) == 1, 'Monitor water quality monitor is empty')
        # Output status without alerts
        self.assertTrue(monitor.output_status() != {}, 'Output status should return a not empty dictionary')
        self.assertFalse(all(['OK' in item for item in monitor.output_status().values()]),
                        'Output status value should not contain OK for all values')


if __name__ == '__main__':
    unittest.main()
