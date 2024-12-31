from src.simulation.water.water import Water
from functools import wraps

class WaterTank:
    """
    A class representing a water tank, which manages and monitors water properties and interactions
    such as evaporation, addition, and extraction.

    The class encapsulates a tank's dimensions, calculates its capacity, manages its water content via
    a `Water` instance, and provides detailed metrics such as evaporation rates and tank status.

    Attributes:
        tank_length (int|float): The length of the tank in centimeters.
        tank_width (int|float): The width of the tank in centimeters.
        tank_depth (int|float): The depth of the tank in centimeters.
        tank_type (str): The type of the tank (e.g., "fish tank", "liquid composter").
        water_surface_area (float): The calculated surface area of the water in the tank.
        total_water_evaporated (float): The total amount of water evaporated from the tank.
        evaporation_rates (dict): A dictionary tracking evaporation rates by air temperature.
    """

    def __init__(self,
                 tank_length: int | float,
                 tank_width: int | float,
                 tank_depth: int | float,
                 tank_type: str):
        """
        Initialize a WaterTank object with dimensions, type, and water capacity.

        Args:
            tank_length (int|float): The length of the tank in centimeters.
            tank_width (int|float): The width of the tank in centimeters.
            tank_depth (int|float): The depth of the tank in centimeters.
            tank_type (str): The type/designation of the tank.

        Raises:
            TypeError: If any tank dimension or type is invalid.
            ValueError: If any tank dimension is negative.
        """
        tank_capacity = (tank_length / 100) * (tank_width / 100) * (tank_depth / 100) * 1000
        self._water_instance = Water(0, tank_capacity)
        self.tank_length = tank_length
        self.tank_width = tank_width
        self.tank_depth = tank_depth
        self.tank_type = tank_type.lower()
        self.water_surface_area = self._define_water_surface_area()
        self.total_water_evaporated = 0
        self.evaporation_rates = {}

    @property
    def status(self):
        """
        Retrieve the current status of the tank.

        The status includes tank dimensions, type, water properties, and evaporation metrics.

        Returns:
            dict: A dictionary containing tank and water-related metrics.
        """
        self._tank_status = {
            "tank_length": self.tank_length,
            "tank_width": self.tank_width,
            "tank_depth": self.tank_depth,
            "tank_type": self.tank_type,
            "water_surface_area": self.water_surface_area}
        self._tank_status.update(self._water_instance.status)
        return self._tank_status

    @property
    def length(self):
        """
        Get or set the tank's length.

        Returns:
            int | float: The length of the tank in centimeters.

        Raises:
            ValueError: If the length is negative.
            TypeError: If the length is not numeric.
        """
        return self.tank_length

    @property
    def width(self):
        """
        Get or set the tank's width.

        Returns:
            int | float: The width of the tank in centimeters.

        Raises:
            ValueError: If the width is negative.
            TypeError: If the width is not numeric.
        """
        return self.tank_width

    @property
    def depth(self):
        """
        Get or set the tank's depth.

        Returns:
            int | float: The depth of the tank in centimeters.

        Raises:
            ValueError: If the depth is negative.
            TypeError: If the depth is not numeric.
        """
        return self.tank_depth

    def __getattr__(self, attribute_name):
        """
        Delegate attribute access to the Water instance.

        If the requested attribute or method exists in the associated Water instance,
        it is returned. Special handling is implemented for the `evaporate` method to
        track evaporation metrics.

        Args:
            attribute_name (str): The name of the requested attribute.

        Returns:
            Any: The corresponding attribute/method from the Water instance.

        Raises:
            AttributeError: If the attribute does not exist in either the WaterTank or Water class.
        """
        # Attempt to retrieve the attribute from the `_water_instance`
        obj_attribute = getattr(self._water_instance, attribute_name, None)
        if obj_attribute is None:
            raise AttributeError(f"Neither '{type(self).__name__}' nor '{type(self._water_instance).__name__}' "
                                 f"object has attribute '{attribute_name}'")

        # Handle callable attributes: special case for 'evaporate'
        if callable(obj_attribute):
            if attribute_name == "evaporate":
                @wraps(obj_attribute)
                def wrapper(*args, **kwargs):
                    # Invoke the 'evaporate' method and track evaporated water
                    water_evaporated = obj_attribute(*args, **kwargs)
                    self.total_water_evaporated += water_evaporated

                    # Extract `air_temp` and `time_elapsed_sec` for metrics
                    air_temp = kwargs.get("air_temp", args[0] if args else 0)
                    time_elapsed_sec = kwargs.get("time_elapsed_sec", args[-1] if args else 1)

                    # Calculate evaporation rate if evaporation occurred
                    if self.water_surface_area > 0 and water_evaporated > 0:
                        evaporation_rate = (water_evaporated / self.water_surface_area) / time_elapsed_sec
                        self.evaporation_rates[air_temp] = evaporation_rate

                    return water_evaporated

                return wrapper

            else:
                return obj_attribute  # Return other methods unmodified
        else:
            # Return non-callable attributes directly
            return obj_attribute

    def _define_water_surface_area(self):
        """
        Calculate the water surface area based on tank type and dimensions.

        Returns:
            float: The water surface area in square meters. If the tank type is unsupported,
                   the result is 0 because that means the water tank is sealed from ambient air.
        """
        if self.tank_type in ("fish tank", "liquid composter"):
            return (self.tank_length / 100) * (self.tank_width / 100)
        else:
            return 0