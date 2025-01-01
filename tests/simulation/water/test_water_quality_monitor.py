import unittest
from src.simulation.water.water_quality_monitor import WaterQualityMonitor
from src.simulation.water.water_property_range import WaterPropertyRange


class TestWaterQualityMonitor(unittest.TestCase):
    """
        Unit tests for the WaterQualityMonitor class.

        This test suite includes tests for initialization, data validation, data analysis, alert generation, and
        output status of the WaterQualityMonitor class.

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

        Ensures that the WaterQualityMonitor is correctly initialized with the given water property ranges and
        that initial alerts and status are empty.

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

        This test checks if the WaterQualityMonitor correctly validates water quality data against predefined
        acceptable ranges for pH, turbidity, temperature, and TDS.

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

        This test checks if the WaterQualityMonitor correctly identifies data within acceptable limits for pH,
        turbidity, temperature, and TDS.

        It initializes the WaterQualityMonitor with predefined ranges for each parameter and verifies that
        the analyze_data method returns True for data within these ranges.
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

        This test checks if the analyze_data method correctly identifies when the water quality data is out of
        the specified acceptable ranges for each parameter.

        It initializes the WaterQualityMonitor with predefined ranges for pH, turbidity, temperature, and TDS,
        and then verifies that the method returns False when the temperature is out of range.

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

        This test checks if the WaterQualityMonitor correctly identifies and alerts when a parameter value is outside
        the specified range.

        It sets up a WaterQualityMonitor with defined ranges for pH, turbidity, temperature, and TDS, then provides
        data with an out-of-range temperature value to verify that an alert is generated.

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

        This test checks if the water quality monitor correctly validates and analyzes data within specified
        ranges for pH, turbidity, temperature, and TDS. It ensures that the monitor outputs a status without alerts
        when data is within acceptable ranges.

        Raises:
            AssertionError: If any of the assertions fail, indicating a problem with data validation, analysis,
            or output status.
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

            This test checks if the water quality monitor correctly identifies and handles out-of-range values for
            various water properties such as pH, turbidity, temperature, and TDS. It ensures that the monitor
            generates alerts for out-of-range values and that the output status reflects these alerts.

            Raises:
                AssertionError: If the data validation or analysis does not behave as expected, or if the output
                status does not correctly reflect the alerts.
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
