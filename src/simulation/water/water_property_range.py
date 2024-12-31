# src/simulation/water/water_property_range.py

class WaterPropertyRange:
    """
    A class representing a range for various properties with specified lower and upper bounds.

    Attributes:
        properties_ranges (dict): A dictionary containing default lower and upper bounds for various properties.

    Methods:
        __init__(property_name, lower_bound, upper_bound): Initializes a PropertyRange object with specified property name, lower bound, and upper bound.
        property_name: Gets or sets the name of the property.
        lower_bound: Gets or sets the lower bound of the property range.
        upper_bound: Gets or sets the upper bound of the property range.
        __repr__(): Returns a string representation of the PropertyRange object.
    """
    properties_ranges = {
        "temperature": {"lower_bound": -30, "upper_bound": 100},
        "ph": {"lower_bound": 0, "upper_bound": 14},
        "turbidity": {"lower_bound": 0, "upper_bound": 1000},
        "viscosity": {"lower_bound": 0, "upper_bound": 1.79},
        "tds": {"lower_bound": 0, "upper_bound": 10000},
        "surface_area": {"lower_bound": 0, "upper_bound": 10000},
        "relative_humidity": {"lower_bound": 0, "upper_bound": 100}
    }

    def __init__(self, property_name, lower_bound, upper_bound):
        self.property_name = property_name
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    @property
    def property_name(self) -> str:
        """
        Get the name of the property associated with this range.

        Returns:
            str: The name of the property.
        """
        return self._property_name

    @property_name.setter
    def property_name(self, value: str):

        """
        Set the property name with validation checks.

        Args:
            value (str): The new property name to set.

        Raises:
            TypeError: If the value is not a string.
            ValueError: If the value is an empty string or not a valid property name.

        """
        if not isinstance(value, str):
            raise TypeError("Property name must be a string.")
        elif len(value) == 0:
            raise ValueError("Property name cannot be empty.")
        elif value not in self.properties_ranges.keys():
            raise ValueError(f"{value} is not a valid property name.")
        self._property_name = value

    @property
    def lower_bound(self) -> float | int:
        """
        Get the lower bound value.

        Returns:
            The lower bound value.
        """
        return self._lower_bound

    @lower_bound.setter
    def lower_bound(self, value: float):
        """
        Set the lower bound value ensuring it is a non-negative number and less than the upper bound.

        Args:
            value (float): The new lower bound value.

        Raises:
            ValueError: If the value is not a non-negative number or if it is not less than the upper bound.
        """
        if not isinstance(value, (float, int)):
            raise ValueError("Lower bound must be a numeric value.")
        elif hasattr(self, "upper_bound") and value >= self.upper_bound:
            raise ValueError("Lower bound must be less than the upper bound.")

        value_range = self.properties_ranges[self.property_name]
        lower_bound = value_range["lower_bound"]
        upper_bound = value_range["upper_bound"]
        if not lower_bound <= value <= upper_bound:
            raise ValueError(f"Lower bound must be between {lower_bound} and {upper_bound} for {self.property_name}.")

        self._lower_bound = value

    @property
    def upper_bound(self) -> float | int:
        """
        Get the upper bound value.

        Returns:
            float: The upper bound value.
        """
        return self._upper_bound

    @upper_bound.setter
    def upper_bound(self, value: float):
        """
        Set the upper bound value ensuring it is a non-negative float and greater than the lower bound.

        Args:
            value (float): The new upper bound value.

        Raises:
            ValueError: If the value is not a non-negative float or if it is not greater than the lower bound.
        """
        if not isinstance(value, (float, int)) or value < 0:
            raise ValueError("Upper bound must be a non-negative floating-point number.")
        elif hasattr(self, "lower_bound") and value <= self.lower_bound:
            raise ValueError("Upper bound must be greater than the lower bound.")

        value_range = self.properties_ranges[self.property_name]
        lower_bound = value_range["lower_bound"]
        upper_bound = value_range["upper_bound"]
        if not lower_bound <= value <= upper_bound:
            raise ValueError(f"Upper bound must be between {lower_bound} and {upper_bound} for {self.property_name}.")

        self._upper_bound = value

    def __repr__(self):
        return f"{self.property_name.capitalize()}_range(lower={self.lower_bound}, upper={self.upper_bound})"

    def check_property_value(self, value):
        """
        Validate that a given value is within the defined property range.

        This method ensures that the provided value lies between the `lower_bound`
        and `upper_bound` of the property range. If the value is outside the range,
        a `ValueError` is raised.

        Args:
            value (float | int): The value to be checked.

        Raises:
            ValueError: If the value is less than `lower_bound` or greater than `upper_bound`.
        """
        if value < self.lower_bound:
            raise ValueError(f"{value} must be greater than or equal to {self.lower_bound} for {self.property_name}.")
        elif value > self.upper_bound:
            raise ValueError(f"{value} must be less than or equal to {self.upper_bound} for {self.property_name}.")
