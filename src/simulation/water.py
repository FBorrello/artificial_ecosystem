# src/simulation/water.py

class Water:
    def __init__(self, initial_nutrients, tank_capacity):
        self.nutrients = initial_nutrients
        self.tank_capacity = tank_capacity
        self.current_nutrients = initial_nutrients
        self._temperature = 25  # Default temperature in Celsius
        self._ph = 7.0  # Neutral pH
        self._turbidity = 0  # Clear water
        self._viscosity = 1.0  # Default viscosity
        self._tds = 0  # Default TDS value

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if not (-10 <= value <= 100):
            raise ValueError("Temperature must be between -10 and 100 degrees Celsius.")
        self._temperature = value

    @property
    def ph(self):
        return self._ph

    @ph.setter
    def ph(self, value):
        if not (0 <= value <= 14):
            raise ValueError("pH must be between 0 and 14.")
        self._ph = value

    @property
    def turbidity(self):
        return self._turbidity

    @turbidity.setter
    def turbidity(self, value):
        if value < 0:
            raise ValueError("Turbidity cannot be negative.")
        self._turbidity = value

    @property
    def viscosity(self):
        return self._viscosity

    @viscosity.setter
    def viscosity(self, value):
        if value <= 0:
            raise ValueError("Viscosity must be positive.")
        self._viscosity = value

    @property
    def tds(self):
        """Get the Total Dissolved Solids (TDS) value."""
        return self._tds

    @tds.setter
    def tds(self, value):
        """Set the Total Dissolved Solids (TDS) value."""
        if value < 0:
            raise ValueError("TDS cannot be negative.")
        self._tds = value
