# tests/test_water.py

import unittest
from src.simulation.water import Water

class TestWater(unittest.TestCase):

    def setUp(self):
        self.water = Water()

    def test_water_flow(self):
        # Setup a simple terrain with a slope
        terrain = [
            [10, 9],
            [8, 7]
        ]
        initial_water = [[100, 0], [0, 0]]
        self.water.set_water_volume(initial_water)
        self.water.flow_water(terrain)
        # Water should have moved from the highest point to the lowest
        self.assertAlmostEqual(self.water.get_water_volume()[1][1], 100, places=2)

    def test_evaporation(self):
        # Test evaporation with known conditions
        self.water.set_water_volume([[1000]])  # 1 liter of water
        self.water.evaporate_water(30, 1)  # 30°C, 1m² surface area
        # Assuming evaporation rate calculation, let's say about 5% evaporated
        self.assertLess(self.water.get_water_volume()[0][0], 950)

    def test_add_precipitation(self):
        self.water.set_water_volume([[0]])
        self.water.add_precipitation("rain", 10)  # 10 units of rain
        self.assertEqual(self.water.get_water_volume()[0][0], 10)

    def test_update_storage_capacity(self):
        # Test with different soil types and structures
        self.water.update_storage_capacity('clay', structures=False)
        self.assertLess(self.water.get_storage_capacity(), 100)  # Clay has lower capacity
        self.water.update_storage_capacity('sand', structures=True)
        self.assertGreater(self.water.get_storage_capacity(), 100)  # Sand with structure has higher capacity

if __name__ == '__main__':
    unittest.main()