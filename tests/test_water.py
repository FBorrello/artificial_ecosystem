import unittest
from src.simulation.water import Water  # Ensure the import path is correct

class TestWater(unittest.TestCase):

    def test_init(self):
        initial_nutrients = 50
        tank_capacity = 200
        water = Water(initial_nutrients, tank_capacity)

        self.assertEqual(water.nutrients, initial_nutrients)
        self.assertEqual(water.tank_capacity, tank_capacity)
        self.assertEqual(water.current_nutrients, initial_nutrients)
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

if __name__ == '__main__':
    unittest.main()
