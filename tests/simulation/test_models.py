# tests/test_models.py
import unittest
from src.simulation.models import Fish
from src.simulation.models import Plant
from src.simulation.models import Environment


class TestFish(unittest.TestCase):
    """
    A class to test the Fish class and its methods.

    This class contains methods to test various functionalities of the Fish class,
    ensuring that all methods work as expected under different scenarios.
    """

    def setUp(self):
        """Set up common test data before each test method."""
        self.non_predatory_fish = Fish("Goldfish", 5, 100, 0)
        self.predatory_fish = Fish("Shark", 100, 150, 5, is_predatory=True)

    def test_fish_creation(self):
        """Test if Fish instances are created with correct initial attributes."""
        self.assertEqual(self.non_predatory_fish.species, "Goldfish")
        self.assertEqual(self.predatory_fish.species, "Shark")
        self.assertTrue(self.predatory_fish.is_predatory)

    def test_move(self):
        """Test the move method of the Fish class."""
        initial_position = self.non_predatory_fish.position.copy()
        self.non_predatory_fish.move


class TestPlant(unittest.TestCase):
    """
    A class to test the Plant class and its methods.

    This class contains methods to test various functionalities of the Plant class,
    ensuring that all methods work as expected under different scenarios.
    """

    def setUp(self):
        """Set up common test data before each test method."""
        self.plant = Plant("Algae", 1, 100, {"nitrogen": 10, "phosphorus": 5})

    def test_plant_creation(self):
        """Test if Plant instances are created with correct initial attributes."""
        self.assertEqual(self.plant.species, "Algae")
        self.assertEqual(self.plant.growth_rate, 1)
        self.assertEqual(self.plant.health, 100)

    def test_growth(self):
        """Test the grow method of the Plant class."""
        initial_health = self.plant.health
        self.plant.grow()
        self.assertEqual(self.plant.health, initial_health + self.plant.growth_rate)

    def test_nutrient_absorption(self):
        """Test the nutrient absorption process."""
        nutrients = {"nitrogen": 15, "phosphorus": 10}
        initial_health = self.plant.health
        self.plant.absorb_nutrients(nutrients)
        # Check if health increased and nutrients decreased
        self.assertTrue(self.plant.health > initial_health)
        self.assertEqual(nutrients["nitrogen"], 5)  # 15 - 10 (required by plant)
        self.assertEqual(nutrients["phosphorus"], 5)  # 10 - 5 (required by plant)

    def test_oxygen_production(self):
        """Test the oxygen production calculation."""
        oxygen = self.plant.produce_oxygen()
        expected_oxygen = self.plant.health * 0.01
        self.assertEqual(oxygen, expected_oxygen)

    def test_plant_str(self):
        """Test the string representation of the Plant instance."""
        plant_str = str(self.plant)
        expected_str = "Algae plant with health 100, growth rate 1"
        self.assertEqual(plant_str, expected_str)


class TestEnvironment(unittest.TestCase):
    """
    A class to test the Environment class and its methods.

    This class contains methods to test various functionalities of the Environment class,
    ensuring that all methods work as expected under different scenarios.
    """

    def setUp(self):
        """Set up common test data before each test method."""
        self.environment = Environment(25, 100, {"nitrogen": 50, "phosphorus": 30}, 7.0)

    def test_environment_creation(self):
        """Test if Environment instances are created with correct initial attributes."""
        self.assertEqual(self.environment.temperature, 25)
        self.assertEqual(self.environment.light_level, 100)
        self.assertEqual(self.environment.nutrients, {"nitrogen": 50, "phosphorus": 30})
        self.assertEqual(self.environment.ph_level, 7.0)

    def test_adjust_temperature(self):
        """Test the temperature adjustment method."""
        initial_temp = self.environment.temperature
        self.environment.adjust_temperature(10)
        self.assertEqual(self.environment.temperature, initial_temp + 10)

    def test_adjust_light(self):
        """Test the light level adjustment method."""
        initial_light = self.environment.light_level
        self.environment.adjust_light(-50)
        self.assertEqual(self.environment.light_level, max(0, initial_light - 50))


if __name__ == '__main__':
    unittest.main()