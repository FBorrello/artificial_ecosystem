# tests/tests_water.py

import unittest
from random import randint

from src.simulation.water.water import Water
from src.simulation.water.water_property_range import WaterPropertyRange
from src.simulation.water.water_quality_monitor import WaterQualityMonitor
from src.simulation.water.water_tank import WaterTank
from src.simulation.water.water_dissolved_elements_monitor import WaterDissolvedElementsMonitor


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
        self.assertEqual(water.viscosity, 0.00089)
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
        valid_temperatures = [0, 25, 50, 100]
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
        """Test the default viscosity value of pure water at 25 degrees Celsius."""
        self.assertEqual(self.water.viscosity, 0.00089, "Default viscosity should be 0.00089")

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

    def test_empirical_viscosity_based_on_water_temperature(self):
        expected_viscosity_by_temp = {25: 0.00089, 50: 0.00054, 100: 0.00028}
        for temp, expected_viscosity in expected_viscosity_by_temp.items():
            with self.subTest(temp=temp):
                self.water.temperature = temp
                self.assertAlmostEqual(self.water.viscosity, expected_viscosity, 4,
                                 f"Viscosity should be based on temperature, "
                                 f"expected viscosity to be {expected_viscosity} for temperature {temp}")

    def test_change_viscosity_according_with_water_temperature_change(self):
        """
        Test the relationship between water temperature changes and viscosity.
    
        This test verifies the following:
        - Viscosity decreases as the temperature increases, simulating real-world physical behavior.
        - Viscosity increases as the temperature decreases.
        - The test uses temperature increments and decrements in a loop, ensuring changes
          are reflected correctly in the viscosity property.
    
        Assertions:
        - Viscosity decreases when the temperature is increased in steps.
        - Viscosity increases when the temperature is decreased in steps.
        """
        initial_viscosity = self.water.viscosity  # Store the initial viscosity for comparison
    
        # Test the effect of increasing temperature on viscosity
        for increment in range(1, 6):
            with self.subTest(increment=increment):
                self.water.temperature += 10  # Increment temperature by 10 units
                self.assertLess(self.water.viscosity, initial_viscosity,
                                'Viscosity should decrease as temperature increases')  # Check viscosity decreases
                initial_viscosity = self.water.viscosity  # Update the reference viscosity for the next iteration
    
        # Test the effect of decreasing temperature on viscosity
        for decrement in range(1, 6):
            with self.subTest(decrement=decrement):
                self.water.temperature -= 10  # Decrement temperature by 10 units
                self.assertGreater(self.water.viscosity, initial_viscosity,
                                'Viscosity should increase as temperature decreases')  # Check viscosity increases
                initial_viscosity = self.water.viscosity  # Update the reference viscosity for the next iteration

    def test_change_viscosity_according_with_water_tds_change(self):
        """
        Test the relationship between water TDS (Total Dissolved Solids) and viscosity.
    
        This test verifies the following:
        - Viscosity increases as the TDS increases, simulating real-world behavior.
        - Viscosity decreases as the TDS decreases.
        - The test iterates over TDS increments and decrements, ensuring changes are reflected
          correctly in the viscosity property.
    
        Assertions:
        - Viscosity increases when TDS is incremented in steps.
        - Viscosity decreases when TDS is decremented in steps.
        """
        initial_viscosity = self.water.viscosity  # Store initial viscosity for reference
    
        # Test the effect of increasing TDS on viscosity
        for increment in range(1, 6):
            with self.subTest(increment=increment):
                self.water.tds += 10000  # Increment TDS by 100 units
                # Verify that viscosity increases as TDS increases
                self.assertGreater(self.water.viscosity, initial_viscosity,
                                'Viscosity should increase as TDS increases')
                initial_viscosity = self.water.viscosity  # Update reference viscosity
    
        # Test the effect of decreasing TDS on viscosity
        for decrement in range(1, 6):
            with self.subTest(decrement=decrement):
                self.water.tds -= 10000  # Decrement TDS by 100 units
                # Verify that viscosity decreases as TDS decreases
                self.assertLess(self.water.viscosity, initial_viscosity,
                                'Viscosity should decrease as TDS decreases')
                initial_viscosity = self.water.viscosity  # Update reference viscosity

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

class TestWaterCurrentVolume(unittest.TestCase):

    def setUp(self):
        """Set up a Water instance for testing."""
        self.water = Water(initial_nutrients=50, tank_capacity=200)

    def test_default_current_volume(self):
        """Test the default current volume value."""
        self.assertEqual(self.water.current_volume, 0, "Default current volume should be 0")

    def test_set_valid_current_volume(self):
        """Test setting a valid current volume."""
        valid_volumes = [0, 50, 200]
        for volume in valid_volumes:
            with self.subTest(volume=volume):
                self.water.current_volume = volume
                self.assertEqual(self.water.current_volume, volume, f"Current volume should be set to {volume} liters")

    def test_set_invalid_current_volume(self):
        """Test setting an invalid current volume raises ValueError."""
        invalid_volumes = [-10, 250]  # Negative value and exceeding capacity
        for volume in invalid_volumes:
            with self.subTest(volume=volume):
                with self.assertRaises(ValueError, msg=f"Setting current volume to {volume} should raise ValueError"):
                    self.water.current_volume = volume

    def test_current_volume_exceeding_capacity(self):
        """Test behavior when current volume exceeds tank capacity."""
        with self.assertRaises(ValueError, msg="Current volume cannot exceed tank capacity"):
            self.water.current_volume = self.water.tank_capacity + 10

class TestWaterUnderflowCapacityThreshold(unittest.TestCase):
    def setUp(self):
        """
        Set up a Water instance and define the underflow capacity threshold.
        """
        self.water = Water(initial_nutrients=50, tank_capacity=200)
        self.water.underflow_capacity_threshold = 20

    def test_default_underflow_capacity_threshold(self):
        """
        Test the default value of the underflow capacity threshold.
        """
        self.assertEqual(self.water.underflow_capacity_threshold, 20,
                         "Default underflow capacity threshold should be 20.")

    def test_set_valid_underflow_capacity_threshold(self):
        """
        Test setting a valid underflow capacity threshold.
        """
        valid_thresholds = [10, 15, 30]
        for threshold in valid_thresholds:
            with self.subTest(threshold=threshold):
                self.water.underflow_capacity_threshold = threshold
                self.assertEqual(self.water.underflow_capacity_threshold, threshold,
                                 f"Underflow capacity threshold should be set to {threshold}.")

    def test_set_invalid_underflow_capacity_threshold(self):
        """
        Test setting an invalid underflow capacity threshold raises ValueError.
        Invalid values include negative numbers or values greater than the tank capacity.
        """
        invalid_thresholds = [-10, 250]
        for threshold in invalid_thresholds:
            with self.subTest(threshold=threshold):
                with self.assertRaises(ValueError,
                                       msg=f"Setting underflow capacity threshold to {threshold} should raise ValueError"):
                    self.water.underflow_capacity_threshold = threshold

class TestWaterOverflowCapacityThreshold(unittest.TestCase):
    def setUp(self):
        """
        Set up a Water instance and define the overflow capacity threshold.
        """
        self.water = Water(initial_nutrients=50, tank_capacity=200)
        self.water.overflow_capacity_threshold = 180

    def test_default_overflow_capacity_threshold(self):
        """
        Test the default value of the overflow capacity threshold.
        """
        self.assertEqual(self.water.overflow_capacity_threshold, 180,
                         "Default overflow capacity threshold should be 180.")

    def test_set_valid_overflow_capacity_threshold(self):
        """
        Test setting a valid overflow capacity threshold.
        """
        valid_thresholds = [150, 160, 190]
        for threshold in valid_thresholds:
            with self.subTest(threshold=threshold):
                self.water.overflow_capacity_threshold = threshold
                self.assertEqual(self.water.overflow_capacity_threshold, threshold,
                                 f"Overflow capacity threshold should be set to {threshold}.")

    def test_set_invalid_overflow_capacity_threshold(self):
        """
        Test setting an invalid overflow capacity threshold raises ValueError.
        Invalid values include negative numbers or values greater than the tank capacity.
        """
        invalid_thresholds = [-10, 250]
        for threshold in invalid_thresholds:
            with self.subTest(threshold=threshold):
                with self.assertRaises(ValueError,
                                       msg=f"Setting overflow capacity threshold to {threshold} should raise ValueError"):
                    self.water.overflow_capacity_threshold = threshold

class TestWaterStatus(unittest.TestCase):
    def setUp(self):
        self.water = Water(initial_nutrients=50, tank_capacity=200)
        self.water.underflow_capacity_threshold = 20
        self.water.overflow_capacity_threshold = 180
    def test_default_status(self):
        water_tank_status = self.water.status
        self.assertEqual(25, water_tank_status.get('temperature'), f"Water temperature should be 25")
        self.assertEqual(7, water_tank_status.get('ph'), f"Water pH should be 7")
        self.assertEqual(0, water_tank_status.get('tds'), f"Water TDS should be 0")
        self.assertEqual(0.00089, water_tank_status.get('viscosity'), f"Water viscosity should be 0")
        self.assertEqual(0, water_tank_status.get('turbidity'), f"Water turbidity should be 0")
        self.assertEqual(0, water_tank_status.get('current_volume'), f"Water current volume should be 0")
        self.assertEqual(20, water_tank_status.get('underflow_capacity_threshold'), f"Water underflow capacity threshold should be 20")
        self.assertEqual(180, water_tank_status.get('overflow_capacity_threshold'), f"Water overflow capacity threshold should be 180")
        self.assertTrue(water_tank_status.get('is_empty'), f"Water tank should be empty")
        self.assertFalse(water_tank_status.get('is_full'), f"Water tank should not be full")
        self.assertEqual(200, water_tank_status.get('tank_capacity'), f"Water tank capacity should be 200")
        self.assertEqual(0, water_tank_status.get('overflow_volume'), f"Water overflow volume should be 0")

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
        melting_rate = int(self.water.temperature ** 2)
        expected_melted_snow = min(amount, melting_rate)
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
        with self.assertRaises(ValueError, msg="Current volume cannot exceed the capacity."):
            self.water.manage_precipitation(precipitation_type, amount, pattern)

class TestWaterEvaporationManagement(unittest.TestCase):
    """
    Test cases for the Water evaporation management system.

    This class tests the evaporation calculation and parameter validations for the Water class.
    """

    def setUp(self):
        """
        Set up a Water instance for testing.

        This is executed before each test case and initializes a Water object with default values.
        """
        self.water = Water(initial_nutrients=50, tank_capacity=200)

    @staticmethod
    def calc_evaporation(air_temp, surface_area, rel_humidity, water_temperature, time_elapsed_sec):
        """
        Calculate the expected evaporation of water over a given time period.

        Uses the Antoine equation for water vapor pressure and relative humidity to calculate
        the evaporation rate, then determines the total evaporation over the specified time.

        Parameters:
        - air_temp (float): Air temperature in degrees Celsius.
        - surface_area (float): Surface area of the exposed water in square meters.
        - rel_humidity (float): Relative humidity as a fraction (0 to 1).
        - water_temperature (float): Temperature of the water in degrees Celsius.
        - time_elapsed_sec (int): Time elapsed in seconds.

        Returns:
        - float: Total evaporation in liters.
        """

        # Constants for the Antoine equation for water
        a_const = 8.07131
        b_const = 1730.63
        c_const = 233.426

        # Calculate the saturation vapor pressure (SVP) of water at the given water temperature
        saturation_vapor_pressure = 10 ** (a_const - (b_const / (c_const + water_temperature)))

        # Calculate the actual vapor pressure (AVP) of air based on relative humidity
        saturation_vapor_pressor_air = rel_humidity * saturation_vapor_pressure

        # Coefficient for the evaporation rate, with adjustment based on temperature difference
        k = 0.1 + 0.01 * (air_temp - water_temperature)

        # Calculate the evaporation rate in grams per hour
        evaporation_rate = k * surface_area * (saturation_vapor_pressure - saturation_vapor_pressor_air)

        # Convert elapsed time from seconds to hours
        time_elapsed_hours = time_elapsed_sec / 3600

        # Calculate total evaporation in grams
        total_evaporation_grams = evaporation_rate * time_elapsed_hours

        # Convert grams to liters since 1 liter = 1000 grams
        total_evaporation_liters = total_evaporation_grams / 1000

        return total_evaporation_liters

    def test_water_evaporation(self):
        """
        Test the evaporation calculation works correctly.

        This test compares the evaporation calculation using the `calc_evaporation` method
        with the evaporation result from the `Water.evaporate` method.
        """

        # Test parameters
        air_temp = 20  # Air temperature in degrees Celsius
        surface_area = 6  # Surface area of the exposed water in square meters
        rel_humidity = 0.5  # Relative humidity as a fraction
        water_temperature = 10  # Water temperature in degrees Celsius
        time_elapsed = 600  # Time elapsed in seconds

        # Calculate expected evaporation using static method
        expected_water_evaporation = self.calc_evaporation(air_temp, surface_area, rel_humidity, water_temperature,
                                                           time_elapsed)

        # Set the water temperature for the test case
        self.water.temperature = water_temperature

        # Set an initial water volume greater than 0
        self.water.current_volume = 100

        # Use the Water class to calculate evaporation
        water_evaporated = self.water.evaporate(air_temp, surface_area, rel_humidity, time_elapsed)

        # Assert that the calculated evaporation matches the expected value
        self.assertEqual(expected_water_evaporation, water_evaporated,
                         "Water evaporation should be calculated correctly")

    def test_water_evaporation_params_out_of_range(self):
        """
        Test parameter validation for out-of-range input values.

        This test ensures that the `Water.evaporate` method raises a ValueError
        when provided with values outside the defined ranges.
        """

        # Access the Water property ranges for validation
        properties_ranges = WaterPropertyRange.properties_ranges

        # Parameters to test, their property mapping, and acceptable ranges
        evaporation_params = [
            {'param_name': 'air_temp', 'property_name': 'temperature'},
            {'param_name': 'surface_area', 'property_name': 'surface_area'},
            {'param_name': 'rel_humidity', 'property_name': 'relative_humidity'}
        ]

        # Generate test cases for lower and upper bound violations
        test_cases = list()
        for property_name, property_range in properties_ranges.items():
            for param_dct in evaporation_params:
                if param_dct['property_name'] == property_name:
                    # Create test case with a value below the lower bound
                    allowed_params_values = {'air_temp': 10, 'surface_area': 6, 'rel_humidity': 0.5,
                                             'time_elapsed_sec': 600}
                    lower_bound = property_range['lower_bound']
                    allowed_params_values[param_dct['param_name']] = lower_bound - 1
                    test_cases.append(allowed_params_values)

                    # Create test case with a value above the upper bound
                    allowed_params_values = {'air_temp': 10, 'surface_area': 6, 'rel_humidity': 0.5,
                                             'time_elapsed_sec': 600}
                    upper_bound = property_range['upper_bound']
                    allowed_params_values[param_dct['param_name']] = upper_bound + 1
                    test_cases.append(allowed_params_values)

        # Check that each test case raises a ValueError
        with self.assertRaises(ValueError):
            for test_case in test_cases:
                self.water.evaporate(**test_case)

    def test_water_evaporation_params_invalid_type(self):
        """
        Test parameter validation for incorrect data types.

        This test ensures that the `Water.evaporate` method raises a TypeError
        when provided with parameters of incorrect data types.
        """

        # Define correct parameter values
        allowed_params_values = {'air_temp': 10, 'surface_area': 6, 'rel_humidity': 0.5, 'time_elapsed_sec': 600}

        # Generate test cases for invalid types
        test_cases = list()
        for param_name, value in allowed_params_values.items():
            # Create a copy of the allowed parameter values
            params_values = {param_name: value for param_name, value in allowed_params_values.items()}

            # Set the current parameter to an invalid type (e.g., string)
            params_values[param_name] = 'invalid_type'
            test_cases.append(params_values)

        # Check that each test case raises a TypeError
        with self.assertRaises(TypeError):
            for test_case in test_cases:
                self.water.evaporate(**test_case)

    def test_water_evaporation_air_temp_below_zero(self):
        """
        Test the evaporation calculation of water when the air temperature is below zero degrees Celsius.

        This test ensures that the `evaporate` method of the `Water` class handles evaporation correctly
        under freezing temperature conditions. It verifies that the calculated evaporation matches the
        expected value obtained using the `calc_evaporation` static method.

        Test Parameters:
        - Air temperature: -10°C
        - Surface area: 10 square meters
        - Relative humidity: 20% (0.2 as a fraction)
        - Water temperature: 0°C
        - Time elapsed: 3600 seconds (1 hour)

        Assertions:
        - The evaporation value calculated using the `evaporate` method of the `Water` class matches
          the expected evaporation value computed using the `calc_evaporation` static method.
        """
        # Test parameters
        air_temp = -10  # Air temperature in degrees Celsius
        surface_area = 10  # Surface area of the exposed water in square meters
        rel_humidity = 0.2  # Relative humidity as a fraction
        water_temperature = 0  # Water temperature in degrees Celsius
        time_elapsed = 3600  # Time elapsed in seconds

        # Calculate expected evaporation using static method
        expected_water_evaporation = self.calc_evaporation(air_temp, surface_area, rel_humidity, water_temperature,
                                                           time_elapsed)

        # Set the water temperature for the test case
        self.water.temperature = water_temperature

        # Use the Water class to calculate evaporation
        water_evaporated = self.water.evaporate(air_temp, surface_area, rel_humidity, time_elapsed)

        # Assert that the calculated evaporation matches the expected value
        self.assertEqual(expected_water_evaporation, water_evaporated,
                         "Water evaporation should be calculated correctly")

    def test_water_evaporation_surface_area_is_zero(self):
        air_temp = 10
        surface_area = 0
        rel_humidity = 0.2
        time_elapsed = 3600

        water_evaporated = self.water.evaporate(air_temp, surface_area, rel_humidity, time_elapsed)

        self.assertEqual(0, water_evaporated, f"Water evaporation should be 0")

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

class TestWaterStorageManagement(unittest.TestCase):
    def setUp(self):
        initial_nutrients = 50
        tank_capacity = 100
        self.water_tank = Water(initial_nutrients, tank_capacity)

    def test_add_rain_precipitation(self):
        """
        Test adding rain precipitation to the water tank.
    
        This test ensures that precipitation in the form of rain increases
        the tank's water volume correctly, given the rain amount.
        
        Test Parameters:
        - Rain amount: 10 liters
        - Precipitation type: 'rain'
    
        Procedure:
        - Retrieve the initial water volume before precipitation.
        - Simulate the addition of rain using the `manage_precipitation` method.
        - Calculate the expected volume after precipitation.
        - Compare the actual water volume to the expected value.
    
        Assertions:
        - The water tank's current volume should match the calculated expected volume.
    
        Raises:
        AssertionError: If the calculated volume does not match the tank's actual volume after precipitation.
        """
        # Define the rain amount to be added (in liters)
        rain_amount = 10
    
        # Retrieve the current water volume before precipitation
        current_volume = self.water_tank.current_volume
    
        # Simulate the addition of rain to the tank
        self.water_tank.manage_precipitation('rain', rain_amount, 'steady')
    
        # Calculate the expected volume after precipitation
        expected_volume = current_volume + rain_amount
    
        # Assert that the tank's current volume matches the expected volume
        self.assertEqual(expected_volume,
                         self.water_tank.current_volume,
                         f'After rain amount {rain_amount} liters, the volume should be {expected_volume} '
                         f'from previous volume {current_volume}')

    def test_add_rain_precipitation_over_capacity(self):
        """
        Test handling of rain precipitation exceeding the tank's capacity.

        This test verifies the following:
        - Adding rain that exceeds the tank's predefined capacity raises a ValueError.
        - The water tank's volume does not exceed its maximum capacity after attempting
          to add excessive precipitation.
        - The appropriate error message is raised when the remaining capacity is insufficient.

        Test Parameters:
        - Rain amount: 110 liters
        - Precipitation type: 'rain'

        Assertions:
        - A ValueError is raised when the rain amount exceeds the tank's capacity.
        - The error message is "Current volume cannot exceed the capacity."
        """
        # Set the rain amount to be added to the tank
        rain_amount = 110

        # Expect Value error the rain amount exceeded the capacity
        with self.assertRaises(ValueError, msg="Current volume should not exceed tank's capacity.") as context:
            # Add precipitation of rain to the tank using the appropriate method
            self.water_tank.manage_precipitation('rain', rain_amount, 'steady')

        # Ensure the exception message matches when current volume is 0
        self.assertEqual(str(context.exception), "Current volume cannot exceed the tank's capacity.")

    def test_add_rain_precipitation_over_capacity_overflow_value(self):
        expected_overflow_volume = 50
        rain_amount = self.water_tank.tank_capacity + expected_overflow_volume

        with self.assertRaises(ValueError, msg="Current volume should not exceed tank's capacity."):
            self.water_tank.manage_precipitation('rain', rain_amount, 'steady')

        self.assertEqual(expected_overflow_volume, self.water_tank.overflow_volume,
                         f'Current overflow volume should be {expected_overflow_volume}.')

    def test_evaporation(self):
        """
        Test the evaporation functionality of the Water class.
    
        This test case verifies the following:
        - Evaporation reduces the current water volume correctly.
        - It calculates the evaporated water using provided environmental parameters
          like air temperature, surface area, relative humidity, and time elapsed.
        - It ensures the final water volume matches the expected result based on
          the evaporation calculations.
        """
        # Set the initial water volume in the tank
        current_volume = 100
        self.water_tank.current_volume = current_volume
    
        # Define environmental parameters for evaporation
        air_temp = 30  # Air temperature in degrees Celsius
        surface_area = 10  # Surface area of exposed water in sq. meters
        rel_humidity = 0.5  # Relative humidity as a fraction
        time_elapsed = 10000  # Time elapsed in seconds
    
        # Perform evaporation calculation and get the water evaporated
        water_evaporated = self.water_tank.evaporate(air_temp, surface_area, rel_humidity, time_elapsed)
    
        # Calculate the expected water volume after evaporation
        expected_volume = current_volume - water_evaporated
    
        # Assert that the water volume matches the expected volume
        self.assertEqual(expected_volume,
                         self.water_tank.current_volume,
                         f'After evaporation amount {water_evaporated} liters, the volume should be '
                         f'{expected_volume} from previous volume {current_volume}')

    def test_evaporation_empty_tank(self):
        """
        Test the evaporation functionality for an empty water tank.
    
        This test ensures that attempting to evaporate water from an empty tank raises a ValueError.
        It verifies the robustness of the `evaporate` method in handling situations where there is
        insufficient water for evaporation.
    
        Raises:
            ValueError: If evaporation is attempted with zero current volume.
        """
        # Define environmental parameters for evaporation
        air_temp = 30  # Air temperature in degrees Celsius
        surface_area = 10  # Surface area of the exposed water in square meters
        rel_humidity = 0.5  # Relative humidity as a fraction
        time_elapsed = 10000  # Time elapsed in seconds
    
        # Expect a ValueError since the water tank is empty (current_volume = 0 by default)
        with self.assertRaises(ValueError) as context:
            self.water_tank.evaporate(air_temp, surface_area, rel_humidity, time_elapsed)

        # Ensure the exception message matches when current volume is 0
        self.assertEqual(str(context.exception), "Current volume must be non-negative.")
    
    def test_water_underflow_management(self):
        """
        Test water underflow management in the tank.
    
        This test verifies that extracting water from the tank works as expected when the underflow capacity threshold
        is enforced. If water extraction exceeds the underflow threshold, a ValueError is raised.
    
        Steps:
        - Add 50 liters of precipitation to the tank.
        - Attempt to extract an amount exceeding the underflow capacity threshold.
        - Verify that a ValueError is raised with the appropriate error message.
    
        Assertions:
        - A ValueError is raised if the water amount extracted exceeds the underflow threshold.
        """
        self.water_tank.manage_precipitation('rain', 50)
        with self.assertRaises(ValueError, 
                               msg="The current volume to extract cannot exceed the underflow capacity threshold."):
            self.water_tank.extract_water(45)

    def test_water_tank_from_empty_to_full(self):
        """
        Test the behavior of the water tank when transitioning from empty to full.
    
        This test iterates over a range of values from 0 (empty tank) to the tank's maximum capacity,
        verifying the `is_empty` and `is_full` properties of the water tank. It ensures that:
        - The tank is marked as empty when the current volume is less than or equal to the underflow capacity threshold.
        - The tank is marked as full when the current volume exceeds the overflow capacity threshold.
        - All other states are categorized appropriately as neither empty nor full.
        """
        for increment in range(self.water_tank.tank_capacity + 1):  # Iterate from 0 to the tank’s capacity
            with self.subTest(increment=increment):
                self.water_tank.current_volume = increment  # Set the tank volume at each step
    
                # Validate the is_empty property
                if increment <= self.water_tank.underflow_capacity_threshold:
                    self.assertTrue(self.water_tank.is_empty, 
                                    f"Tank should be empty when volume is {increment} or below the threshold.")
                else:
                    self.assertFalse(self.water_tank.is_empty, 
                                     f"Tank should not be empty when volume is above the threshold.")
    
                # Validate the is_full property
                if increment >= self.water_tank.tank_capacity - self.water_tank.overflow_capacity_threshold:
                    self.assertTrue(self.water_tank.is_full, 
                                    f"Tank should be full when volume is {increment} or above the threshold.")
                else:
                    self.assertFalse(self.water_tank.is_full, 
                                     f"Tank should not be full when volume is below the threshold.")

class TestWaterAddWater(unittest.TestCase):
    """
    Unit tests for the `add_water` method in the Water class.
    """

    def setUp(self):
        """
        Set up a Water instance for testing.
        """
        self.water_tank = Water(initial_nutrients=50, tank_capacity=200)
        self.water_tank.current_volume = 100  # Initial water level set to 100 for testing.

    def test_add_valid_water_volume(self):
        """
        Test adding water with a valid volume.
        """
        initial_volume = self.water_tank.current_volume
        volume_to_add = 50

        self.water_tank.add_water(volume_to_add)

        expected_volume = initial_volume + volume_to_add
        self.assertEqual(expected_volume, self.water_tank.current_volume,
                         f"After adding {volume_to_add} liters, the volume should be {expected_volume}.")
        self.assertEqual(self.water_tank.current_volume, expected_volume,
                         "Current volume should match the result of adding water.")

    def test_add_water_causes_overflow(self):
        """
        Test adding water that exceeds the tank's capacity.
        """
        volume_to_add = 150  # Exceeds current available capacity.
        with self.assertRaises(ValueError, msg="Adding water beyond capacity should raise ValueError."):
            self.water_tank.add_water(volume_to_add)

    def test_add_invalid_water_volume(self):
        """
        Test adding invalid water volumes (negative or zero values).
        """
        invalid_volumes = [-10, 0]
        for volume in invalid_volumes:
            with self.subTest(volume=volume):
                with self.assertRaises(ValueError, msg=f"Adding {volume} liters should raise ValueError."):
                    self.water_tank.add_water(volume)

class TestWaterExtractWater(unittest.TestCase):
    """
    Unit tests for the `extract_water` method in the Water class.
    """

    def setUp(self):
        """
        Set up a Water instance for testing.
        """
        self.water_tank = Water(initial_nutrients=50, tank_capacity=200)
        self.water_tank.manage_precipitation('rain', 100, 'steady')

    def test_extract_valid_volume(self):
        """
        Test extracting water when the current volume is within allowable range.
        """
        initial_volume = self.water_tank.current_volume
        volume_to_extract = 50

        extracted_volume = self.water_tank.extract_water(volume_to_extract)

        self.assertEqual(extracted_volume, volume_to_extract,
                         f"Extracted volume should be {volume_to_extract}.")
        self.assertEqual(self.water_tank.current_volume, initial_volume - volume_to_extract,
                         f"Current volume should decrease by {volume_to_extract}.")

    def test_extract_underflow_volume(self):
        """
        Test extracting water when the volume goes below the underflow threshold.
        """
        water_amount_to_extract = (self.water_tank.current_volume - self.water_tank.underflow_capacity_threshold) + 10
        with self.assertRaises(ValueError, msg="Extracting volume below the underflow threshold should raise ValueError."):
            self.water_tank.extract_water(water_amount_to_extract)

    def test_extract_invalid_volume(self):
        """
        Test extracting invalid water volume (negative or exceeding the current volume).
        """
        invalid_volumes = [-10, self.water_tank.current_volume + 1]
        for volume in invalid_volumes:
            with self.subTest(volume=volume):
                with self.assertRaises(ValueError, msg=f"Extracting volume {volume} should raise ValueError."):
                    self.water_tank.extract_water(volume)

    def test_extract_entire_volume_forcing_underflow_capacity_threshold(self):
        """
        Test extracting the entire current water volume.
        """
        initial_volume = self.water_tank.current_volume

        extracted_volume = self.water_tank.extract_water(initial_volume, True)

        self.assertEqual(extracted_volume, initial_volume,
                         f"Extracted volume should match the entire tank volume of {initial_volume}.")
        self.assertEqual(self.water_tank.current_volume, 0,
                         "Current volume should be 0 after extracting the entire volume.")

class TestWaterFishTank(unittest.TestCase):
    """
    Unit tests for the WaterTank class for managing a fish tank.

    This test suite includes tests for various functionalities related to the fish tank's status,
    water evaporation handling, total evaporation calculations, and evaporation rate validations.
    """

    def setUp(self):
        """
        Set up a fish tank instance with specific dimensions for testing.

        The fish tank instance is initialized with:
        - Length: 400 units
        - Width: 150 units
        - Depth: 100 units
        - Tank type: 'fish tank'
        """
        self.tank_length = 400
        self.tank_width = 150
        self.tank_depth = 100
        self.fish_tank = WaterTank(self.tank_length, self.tank_width, self.tank_depth, 'fish tank')

    def test_fish_status(self):
        """
        Test the status properties of the fish tank.
    
        This test verifies that the fish tank's dimensions (length, width, depth) and type ('fish tank')
        are correctly set and returned by the status method.
        """
        status = self.fish_tank.status
        self.assertEqual(self.tank_depth, status.get('tank_depth'), f'Depth should be {self.tank_depth}')
        self.assertEqual(self.tank_width, status.get('tank_width'), f'Width should be {self.tank_width}')
        self.assertEqual(self.tank_length, status.get('tank_length'), f'Length should be {self.tank_length}')
        self.assertEqual('fish tank', status.get('tank_type'), f'Tank type should be fish tank')

    def test_evaporation_manager_total_water_evaporated(self):
        """
        Test the total water evaporation calculation over multiple evaporation sessions.

        This test adds water to the fish tank, calculates evaporation across 10 sessions,
        and verifies that the total water evaporated matches the recorded total water evaporated
        property of the fish tank.
        """
        total_water_evaporated = 0
        self.fish_tank.add_water(1000)
        air_temp = 30
        surface_area = self.fish_tank.water_surface_area
        rel_humidity = 0.5
        time_elapsed_sec = 3600
        for session in range(1, 11):
            total_water_evaporated += self.fish_tank.evaporate(air_temp, surface_area, rel_humidity, time_elapsed_sec)
        self.assertEqual(total_water_evaporated, self.fish_tank.total_water_evaporated,
                         f"Total water evaporated should be {self.fish_tank.total_water_evaporated}")

    def test_evaporation_manager_evaporation_rate(self):
        """
        Test the evaporation rate calculation over multiple sessions.

        This test calculates the evaporation rate for the fish tank and verifies that the
        evaporation rate remains consistent across multiple evaporation sessions.
        """
        self.fish_tank.add_water(1000)
        air_temp = 30
        surface_area = self.fish_tank.water_surface_area
        rel_humidity = 0.5
        time_elapsed_sec = 3600
        water_evaporated = self.fish_tank.evaporate(air_temp, surface_area, rel_humidity, time_elapsed_sec)
        expected_evaporation_rate = (water_evaporated / surface_area) / time_elapsed_sec
        for session in range(1, 101):
            time_elapsed_sec = randint(1, 3600)
            with self.subTest(session=session):
                self.fish_tank.evaporate(air_temp, surface_area, rel_humidity, time_elapsed_sec)
                evaporation_rate = self.fish_tank.evaporation_rates.get(air_temp)
                self.assertAlmostEqual(expected_evaporation_rate, evaporation_rate, 10,
                                 f"Evaporation rate should be {expected_evaporation_rate} but is {evaporation_rate}")
    
class TestWaterDissolvedElementsTracker(unittest.TestCase):
    def setUp(self):
        self.initial_properties_ranges = {property_range_name: property_range
                                     for property_range_name, property_range
                                     in WaterPropertyRange.properties_ranges.items()}
        self.water_tank = WaterTank(tank_length=400, tank_width=150, tank_depth=100, tank_type='fish tank')
        self.water_tank.manage_precipitation('rain', 4000, 'steady')
        self.water_dissolved_elements = {
            # Macronutrients
            'ammonia': {'min': 0.1, 'max': 1, 'initial': 0.2},
            'nitrate': {'min': 0.1, 'max': 50, 'initial': 10},
            'nitrite': {'min': 0.1, 'max': 0.5, 'initial': 0.2},
            'phosphate': {'min': 0.1, 'max': 2, 'initial': 0.5},
        
            # Micronutrients
            'potassium': {'min': 1, 'max': 5, 'initial': 2},
            'iron': {'min': 0.1, 'max': 0.5, 'initial': 0.2},
            'magnesium': {'min': 2, 'max': 10, 'initial': 5},
            'calcium': {'min': 20, 'max': 150, 'initial': 40},
        
            # Pollutants from fish metabolism and decomposition
            'hydrogen_sulfide': {'min': 0.1, 'max': 0.5, 'initial': 0.2},
            'organic_debris': {'min': 0.1, 'max': 100, 'initial': 5},

            # Dissolved gas
            'oxygen': {'min': 0.1, 'max': 100, 'initial': 50},
            'carbon_dioxide': {'min': 0.1, 'max': 100, 'initial': 10}
        }
        self.dissolved_elements_monitor = WaterDissolvedElementsMonitor(self.water_tank, self.water_dissolved_elements)

    def tearDown(self):
        WaterPropertyRange.properties_ranges = self.initial_properties_ranges

    def test_init_empty_dict_water_dissolved_elements(self):
        water_dissolved_elements = {}
        self.water_tank = WaterTank(tank_length=400, tank_width=150, tank_depth=100, tank_type='fish tank')
        self.water_tank.manage_precipitation('rain', 4000, 'steady')
        with self.assertRaises(ValueError, msg="Empty dictionary should raise ValueError.") as context:
            self.dissolved_elements_monitor = WaterDissolvedElementsMonitor(self.water_tank, water_dissolved_elements)
        self.assertEqual(str(context.exception), "The dissolved_elements dictionary cannot be empty.")

    def test_init_invalid_type_water_dissolved_elements(self):
        water_dissolved_elements = []
        self.water_tank = WaterTank(tank_length=400, tank_width=150, tank_depth=100, tank_type='fish tank')
        self.water_tank.manage_precipitation('rain', 4000, 'steady')
        error_msg = "water_dissolved_elements not dictionary should raise TypeError."
        with self.assertRaises(TypeError, msg=error_msg) as context:
            self.dissolved_elements_monitor = WaterDissolvedElementsMonitor(self.water_tank, water_dissolved_elements)
        self.assertEqual(str(context.exception), "The dissolved_elements parameter must be a dictionary.")

    def test_init_None_water_dissolved_elements(self):
        with self.assertRaises(TypeError, msg="Invalid water_tank argument should raise TypeError.") as context:
            self.dissolved_elements_monitor = WaterDissolvedElementsMonitor(None,
                                                                            self.water_dissolved_elements)
        self.assertEqual(str(context.exception), "The `water_tank` parameter must be a `WaterTank` instance.")

    def test_add_dissolved_elements_value_within_range(self):
        for element in self.water_dissolved_elements:
            with self.subTest(element=element):
                min_value = int(self.water_dissolved_elements[element]['min'] * 100)
                max_value = int(self.water_dissolved_elements[element]['max'] * 100)
                for value in range(min_value, max_value + 1):
                    value /= 100
                    setattr(self.dissolved_elements_monitor, element, value)
                    modified_value = getattr(self.dissolved_elements_monitor, element)
                    self.assertEqual(value, modified_value,
                                     f"Modified value for {element} should be {value} "
                                     f"not {modified_value}")

    def test_add_dissolved_elements_value_out_of_range(self):
        for element in self.water_dissolved_elements:
            with self.subTest(element=element):
                min_value = self.water_dissolved_elements[element]['min']
                max_value = self.water_dissolved_elements[element]['max']
                out_of_range_min_value = min_value - 0.01
                error_msg = f"Value for {element} should be between {min_value} and {max_value}"
                with self.assertRaises(ValueError, msg=error_msg) as context:
                    setattr(self.dissolved_elements_monitor, element, out_of_range_min_value)
                error_msg = f"{out_of_range_min_value} must be greater than or equal to {min_value} for {element}."
                self.assertEqual(str(context.exception), error_msg)
                out_of_range_max_value = max_value + 0.01
                with self.assertRaises(ValueError, msg=error_msg) as context:
                    setattr(self.dissolved_elements_monitor, element, out_of_range_max_value)
                error_msg = f"{out_of_range_max_value} must be less than or equal to {max_value} for {element}."
                self.assertEqual(str(context.exception), error_msg)

    def test_add_dissolved_elements_value_negative_number(self):
        for element in self.water_dissolved_elements:
            with self.subTest(element=element):
                error_msg = f"Value for {element} should be a non-negative number."
                with self.assertRaises(ValueError, msg=error_msg) as context:
                    setattr(self.dissolved_elements_monitor, element, -1)
                self.assertEqual(str(context.exception), f"{element} concentration must be non-negative.")

    def test_add_dissolved_elements_type_error(self):
        for element in self.water_dissolved_elements:
            with self.subTest(element=element):
                initial_value = getattr(self.dissolved_elements_monitor, element)
                error_msg = f"Setting {element} to a non-numeric value should raise TypeError."
                with self.assertRaises(TypeError, msg=error_msg) as context:
                    setattr(self.dissolved_elements_monitor, element, str(initial_value))
                self.assertEqual(str(context.exception),f"{element} concentration must be a numeric value.")

    def test_evaporation_affect_dissolved_elements_concentration(self):
        dissolved_elements = self.dissolved_elements_monitor._get_dissolved_element_properties()
        dissolved_elements = {element: getattr(self.dissolved_elements_monitor, element)
                              for element in dissolved_elements}
        air_temp = 30
        surface_area = self.water_tank.water_surface_area
        rel_humidity = 0.5
        time_elapsed_sec = 3600
        self.water_tank.evaporate(air_temp, surface_area, rel_humidity, time_elapsed_sec)
        new_dissolved_elements = {element: getattr(self.dissolved_elements_monitor, element)
                                  for element in dissolved_elements}
        for element in new_dissolved_elements:
            with self.subTest(element=element):
                self.assertLess(new_dissolved_elements[element], dissolved_elements[element],
                                f"Dissolved element {element} should decrease.")


if __name__ == '__main__':
    unittest.main()
