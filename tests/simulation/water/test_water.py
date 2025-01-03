# tests/tests_water.py

import unittest
from src.simulation.water.water import Water
from src.simulation.water.water_property_range import WaterPropertyRange


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
        air_temp = 15
        pattern = 'steady'

        initial_volume = self.water.current_volume
        self.water.manage_precipitation(precipitation_type, amount, air_temp, pattern)

        expected_volume = initial_volume + amount
        self.assertEqual(self.water.current_volume, expected_volume,
                         "Water volume should increase by the amount of rain")

    def test_manage_precipitation_snow(self):
        """Test managing precipitation with snow."""
        precipitation_type = 'snow'
        amount = 10
        air_temp = 5
        pattern = 'intermittent'

        initial_volume = self.water.current_volume
        self.water.manage_precipitation(precipitation_type, amount, air_temp, pattern)

        # Calculate expected volume after snow melting
        melting_rate = 0.01 * self.water.snow_accumulation * (air_temp / (air_temp + 5))
        expected_melted_snow = min(amount, melting_rate)
        expected_volume = initial_volume + expected_melted_snow

        self.assertEqual(round(self.water.current_volume, 2), round(expected_volume, 2),
                         "Water volume should reflect snow accumulation and melting")

    def test_invalid_precipitation_type(self):
        """Test handling of invalid precipitation type."""
        with self.assertRaises(ValueError, msg="Invalid precipitation type should raise ValueError"):
            self.water.manage_precipitation('hail', 10, 'steady')

    def test_precipitation_exceeds_capacity(self):
        """Test precipitation management when it exceeds tank capacity."""
        precipitation_type = 'rain'
        amount = 300  # Exceeds tank capacity
        air_temp = 15
        pattern = 'steady'
        with self.assertRaises(ValueError, msg="Current volume cannot exceed the capacity."):
            self.water.manage_precipitation(precipitation_type, amount, air_temp, pattern)

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
        air_temp = 15
    
        # Retrieve the current water volume before precipitation
        current_volume = self.water_tank.current_volume
    
        # Simulate the addition of rain to the tank
        self.water_tank.manage_precipitation('rain', rain_amount, air_temp,'steady')
    
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
        air_temp = 15

        # Expect Value error the rain amount exceeded the capacity
        with self.assertRaises(ValueError, msg="Current volume should not exceed tank's capacity.") as context:
            # Add precipitation of rain to the tank using the appropriate method
            self.water_tank.manage_precipitation('rain', rain_amount, air_temp, 'steady')

        # Ensure the exception message matches when current volume is 0
        self.assertEqual(str(context.exception), "Current volume cannot exceed the tank's capacity.")

    def test_add_rain_precipitation_over_capacity_overflow_value(self):
        expected_overflow_volume = 50
        rain_amount = self.water_tank.tank_capacity + expected_overflow_volume
        air_temp = 15

        with self.assertRaises(ValueError, msg="Current volume should not exceed tank's capacity."):
            self.water_tank.manage_precipitation('rain', rain_amount, air_temp,'steady')

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
        self.water_tank.manage_precipitation('rain', 50, 15, "steady")
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
        self.water_tank.manage_precipitation('rain', 100, 25,'steady')

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


if __name__ == '__main__':
    unittest.main()
