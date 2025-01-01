import unittest
from random import randint
from src.simulation.water.water_tank import WaterTank

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