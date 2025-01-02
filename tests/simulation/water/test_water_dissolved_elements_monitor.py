import unittest
from src.simulation.water.water_dissolved_elements_monitor import WaterDissolvedElementsMonitor
from src.simulation.water.water_property_range import WaterPropertyRange
from src.simulation.water.water_tank import WaterTank


class TestWaterDissolvedElementsTracker(unittest.TestCase):
    """
    A test suite for validating the behavior of the WaterDissolvedElementsMonitor class,
    which manages the dissolved elements in a water tank under various scenarios.

    This test class verifies the correctness of methods and decorations applied
    to water tank operations, including evaporation, precipitation, and the addition
    of water, to ensure that dissolved elements are properly tracked and updated.
    """

    def setUp(self):
        """
        Setup method that initializes common objects used in the tests,
        such as the water tank and its dissolved elements monitor.
        """
        # Create a backup of the class attribute properties_ranges of WaterPropertiesRange class
        self.initial_properties_ranges = {property_range_name: property_range
                                          for property_range_name, property_range
                                          in WaterPropertyRange.properties_ranges.items()}

        # Create and initialize a WaterTank instance with dimensions and type
        self.water_tank = WaterTank(tank_length=400, tank_width=150, tank_depth=100, tank_type='fish tank')

        # Add water to the tank
        self.water_tank.manage_precipitation('rain', 4000, 15,'steady')

        # Define an initial dictionary of dissolved elements with their concentrations
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

        # Create an instance of WaterDissolvedElementsMonitor for testing
        self.dissolved_elements_monitor = WaterDissolvedElementsMonitor(self.water_tank, self.water_dissolved_elements)

    def tearDown(self):
        """
        Cleanup method that restores the water property ranges in WaterPropertyRange 
        to their initial state after each test.
        """
        # Reset the initial WaterPropertyRange properties_ranges class property
        WaterPropertyRange.properties_ranges = self.initial_properties_ranges

    def test_init_empty_dict_water_dissolved_elements(self):
        """
        Test that initializing WaterDissolvedElementsMonitor with an empty dictionary 
        raises a ValueError.
        """
        water_dissolved_elements = {}
        self.water_tank = WaterTank(tank_length=400, tank_width=150, tank_depth=100, tank_type='fish tank')
        self.water_tank.manage_precipitation('rain', 4000, 15, 'steady')
        with self.assertRaises(ValueError, msg="Empty dictionary should raise ValueError.") as context:
            self.dissolved_elements_monitor = WaterDissolvedElementsMonitor(self.water_tank, water_dissolved_elements)
        self.assertEqual(str(context.exception), "The dissolved_elements dictionary cannot be empty.")

    def test_init_invalid_type_water_dissolved_elements(self):
        """
        Test that initializing WaterDissolvedElementsMonitor with a non-dictionary type 
        for dissolved elements raises a TypeError.
        """
        water_dissolved_elements = []
        self.water_tank = WaterTank(tank_length=400, tank_width=150, tank_depth=100, tank_type='fish tank')
        self.water_tank.manage_precipitation('rain', 4000, 15,'steady')
        error_msg = "water_dissolved_elements not dictionary should raise TypeError."
        with self.assertRaises(TypeError, msg=error_msg) as context:
            self.dissolved_elements_monitor = WaterDissolvedElementsMonitor(self.water_tank, water_dissolved_elements)
        self.assertEqual(str(context.exception), "The dissolved_elements parameter must be a dictionary.")

    def test_init_None_water_dissolved_elements(self):
        """
        Test that passing None as the water tank to WaterDissolvedElementsMonitor 
        raises a TypeError.
        """
        with self.assertRaises(TypeError, msg="Invalid water_tank argument should raise TypeError.") as context:
            self.dissolved_elements_monitor = WaterDissolvedElementsMonitor(None,
                                                                            self.water_dissolved_elements)
        self.assertEqual(str(context.exception), "The `water_tank` parameter must be a `WaterTank` instance.")

    def test_add_dissolved_elements_value_within_range(self):
        """
        Test that dissolved element concentrations can be set to values within their 
        specified range without errors.
        """
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
        """
        Test that setting dissolved element concentrations to values outside 
        their specified range raises a ValueError.
        """
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
        """
        Test that setting dissolved element concentrations to a negative value 
        raises a ValueError.
        """
        for element in self.water_dissolved_elements:
            with self.subTest(element=element):
                error_msg = f"Value for {element} should be a non-negative number."
                with self.assertRaises(ValueError, msg=error_msg) as context:
                    setattr(self.dissolved_elements_monitor, element, -1)
                self.assertEqual(str(context.exception), f"{element} concentration must be non-negative.")

    def test_add_dissolved_elements_type_error(self):
        """
        Test that setting dissolved element concentrations to a non-numeric 
        type raises a TypeError.
        """
        for element in self.water_dissolved_elements:
            with self.subTest(element=element):
                initial_value = getattr(self.dissolved_elements_monitor, element)
                error_msg = f"Setting {element} to a non-numeric value should raise TypeError."
                with self.assertRaises(TypeError, msg=error_msg) as context:
                    setattr(self.dissolved_elements_monitor, element, str(initial_value))
                self.assertEqual(str(context.exception), f"{element} concentration must be a numeric value.")

    def test_evaporation_affect_dissolved_elements_concentration(self):
        """
        Test that evaporation increases the concentration of dissolved elements 
        as water volume decreases.
        """
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
                self.assertGreater(new_dissolved_elements[element], dissolved_elements[element],
                                   f"Dissolved element {element} should increase in concentration.")

    def test_add_precipitation_water_affect_dissolved_elements_concentration(self):
        """
        Test that adding precipitation water decreases the concentration of 
        dissolved elements by diluting the tank's contents.
        """
        dissolved_elements = self.dissolved_elements_monitor._get_dissolved_element_properties()
        dissolved_elements = {element: getattr(self.dissolved_elements_monitor, element)
                              for element in dissolved_elements}
        self.water_tank.manage_precipitation('rain', 1000, 15, 'steady')
        new_dissolved_elements = {element: getattr(self.dissolved_elements_monitor, element)
                                  for element in dissolved_elements}
        for element in new_dissolved_elements:
            with self.subTest(element=element):
                self.assertLess(new_dissolved_elements[element], dissolved_elements[element],
                                f"Dissolved element {element} should decrease in concentration.")

    def test_add_water_affect_dissolved_elements_concentration(self):
        """
        Test that adding water decreases the concentration of dissolved elements 
        by diluting the water in the tank.
        """
        dissolved_elements = self.dissolved_elements_monitor._get_dissolved_element_properties()
        dissolved_elements = {element: getattr(self.dissolved_elements_monitor, element)
                              for element in dissolved_elements}
        self.water_tank.add_water(1000)
        new_dissolved_elements = {element: getattr(self.dissolved_elements_monitor, element)
                                  for element in dissolved_elements}
        for element in new_dissolved_elements:
            with self.subTest(element=element):
                self.assertLess(new_dissolved_elements[element], dissolved_elements[element],
                                f"Dissolved element {element} should decrease in concentration.")