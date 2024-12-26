# src/simulation/water.py

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
    properties_ranges={
        "temperature": {"lower_bound": -30, "upper_bound": 100},
        "ph":{"lower_bound": 0, "upper_bound": 14},
        "turbidity":{"lower_bound": 0, "upper_bound": 1000},
        "viscosity":{"lower_bound": 0, "upper_bound": 1.79},
        "tds":{"lower_bound": 0, "upper_bound": 10000},
        "surface_area": {"lower_bound": 1, "upper_bound": 10000},
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
    def property_name(self, value:str):

        """
        Set the property name with validation checks.

                Args:
                    value (str): The new property name to set.

                Raises:
                    TypeError: If the value is not a string.
                    ValueError: If the value is an empty string or not a valid property name.

        """
        if not isinstance(value,str):
            raise TypeError("Property name must be a string.")
        elif len(value)==0:
            raise ValueError("Property name cannot be empty.")
        elif value not in self.properties_ranges.keys():
            raise ValueError(f"{value} is not a valid property name.")
        self._property_name=value

    @property
    def lower_bound(self) -> float|int:
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
    def upper_bound(self) -> float|int:
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

class Water:
    def __init__(self, initial_nutrients, tank_capacity):
        self.nutrients = initial_nutrients
        self.tank_capacity = tank_capacity
        self.current_nutrients = initial_nutrients
        self.current_volume = 0  # Initialize current volume
        self.snow_accumulation = 0  # Initialize snow accumulation
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
        if not (0 <= value <= 100):
            raise ValueError("Temperature must be between 0 and 100 degrees Celsius.")
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

    def manage_precipitation(self, precipitation_type, amount, pattern):
        """Manage precipitation events, adjusting the water volume."""
        if precipitation_type not in ['rain', 'snow']:
            raise ValueError("Invalid precipitation type. Must be 'rain' or 'snow'.")

        if precipitation_type == 'rain':
            self.current_volume += amount
        elif precipitation_type == 'snow':
            # Accumulate snow, which will melt over time
            self.snow_accumulation += amount
            # Simulate melting based on temperature
            if self.temperature > 0:  # Assume snow melts when temperature is above 0°C
                melted_snow = min(self.snow_accumulation, self.temperature)  # Simple melting logic
                self.current_volume += melted_snow
                self.snow_accumulation -= melted_snow

        # Ensure the current volume does not exceed the tank capacity
        if self.current_volume > self.tank_capacity:
            self.current_volume = self.tank_capacity

    def evaporate(self,
                  air_temp: int|float,
                  surface_area: int | float,
                  rel_humidity: int|float,
                  time_elapsed_sec: int) -> int | float:
        if not isinstance(air_temp, (int, float)):
            raise TypeError("Air temperature must be a numeric value.")
        air_temp_range = WaterPropertyRange("temperature", -10, 50)
        if air_temp_range.lower_bound > air_temp or air_temp_range.upper_bound < air_temp:
            raise ValueError(f"Air temperature must be between {air_temp_range.lower_bound} "
                             f"and {air_temp_range.upper_bound} degrees Celsius.")

        if not isinstance(surface_area, (int, float)):
            raise TypeError("Surface area must be a numeric value.")
        surface_are_range = WaterPropertyRange("surface_area", 1, 100)
        if surface_are_range.lower_bound > surface_area or surface_are_range.upper_bound < surface_area:
            raise ValueError(f"Surface area must be between {surface_are_range.lower_bound} "
                             f"and {surface_are_range.upper_bound} square meters.")

        if not isinstance(rel_humidity, (int, float)):
            raise TypeError("Relative humidity must be a numeric value.")
        rel_humidity_range = WaterPropertyRange("relative_humidity", 0, 100)
        if rel_humidity_range.lower_bound > rel_humidity or rel_humidity_range.upper_bound < rel_humidity:
            raise ValueError(f"Relative humidity must be between {rel_humidity_range.lower_bound} "
                             f"and {rel_humidity_range.upper_bound} percent.")

        if not isinstance(time_elapsed_sec, (int, float)):
            raise TypeError("Time must be a numeric value.")

        # Constants for the Antoine equation for water
        a_const = 8.07131
        b_const = 1730.63
        c_const = 233.426

        # Calculate the saturation vapor pressure (SVP) of water at the given temperature
        saturation_vapor_pressure = 10 ** (a_const - (b_const / (c_const + self.temperature)))

        # Calculate the actual vapor pressure (AVP) of air
        saturation_vapor_pressor_air = rel_humidity * saturation_vapor_pressure

        # Coefficient for evaporation rate (this value can vary and can be influenced by air temperature)
        k = 0.1 + 0.01 * (air_temp - self.temperature)

        # Calculate the evaporation rate
        evaporation_rate = k * surface_area * (saturation_vapor_pressure - saturation_vapor_pressor_air)

        # Calculate the total evaporation over the given time period in grams
        time_elapsed_hours = time_elapsed_sec / 3600
        total_evaporation_grams = evaporation_rate * time_elapsed_hours

        # Convert grams to liters (1 liter = 1000 grams)
        total_evaporation_liters = total_evaporation_grams / 1000

        return total_evaporation_liters


class WaterQualityMonitor:
    """
    A class to monitor water quality by analyzing various water properties such as pH, turbidity, temperature, and TDS (Total Dissolved Solids).

    Attributes:
        ph_range (WaterPropertyRange): The acceptable range for pH levels.
        turbidity_range (WaterPropertyRange): The acceptable range for turbidity levels.
        temperature_range (WaterPropertyRange): The acceptable range for temperature levels.
        tds_range (WaterPropertyRange): The acceptable range for Total Dissolved Solids (TDS) levels.
        alerts (list): A list to store alert messages.
        status (dict): A dictionary to store the status of each water property.

    Methods:
        validate_data(water_data): Validates the input water data.
        analyze_data(water_data): Analyzes the water data against the specified ranges.
        generate_alert(parameters, value): Generates an alert if a water property is out of range.
        output_status(): Returns the status of each water property.
    """
    def __init__(self,
                 ph_range: WaterPropertyRange,
                 turbidity_range: WaterPropertyRange,
                 temperature_range: WaterPropertyRange,
                 tds_range: WaterPropertyRange):
        self.ph_range = ph_range
        self.turbidity_range = turbidity_range
        self.temperature_range = temperature_range
        self.tds_range = tds_range
        self._alerts = list()
        self._status = dict()

    @property
    def ph_range(self) -> WaterPropertyRange:
        """
        Get the pH range of the water property.

            Returns:
                WaterPropertyRange: The pH range of the water property.
        """
        return self._ph_range

    @ph_range.setter
    def ph_range(self, value: WaterPropertyRange):
        """
        Set the pH range for the water property.

                Args:
                    value (WaterPropertyRange): The pH range to set.

                Raises:
                    TypeError: If the provided value is not an instance of WaterPropertyRange.

        """
        if not isinstance(value,WaterPropertyRange):
            raise TypeError("PH Range must be an instance of WaterPropertyRange")
        self._ph_range=value

    @property
    def turbidity_range(self)->WaterPropertyRange:
        """
        Get the turbidity range property.

            Returns:
                WaterPropertyRange: The range of turbidity values.

        """
        return self._turbidity_range

    @turbidity_range.setter
    def turbidity_range(self, value: WaterPropertyRange):
        """
        Set the turbidity range for the water property.

            Args:
                value (WaterPropertyRange): The new turbidity range to set.

            Raises:
                TypeError: If the provided value is not an instance of WaterPropertyRange.
        """
        if not isinstance(value, WaterPropertyRange):
            raise TypeError("Turbidity Range must be an instance of WaterPropertyRange")
        self._turbidity_range=value

    @property
    def temperature_range(self)->WaterPropertyRange:
        """

            Get the temperature range property.

            Returns:
                WaterPropertyRange: The temperature range of the water property.

        """
        return self._temperature_range

    @temperature_range.setter
    def temperature_range(self, value: WaterPropertyRange):
        """
        Set the temperature range for the water property.

            Args:
                value (WaterPropertyRange): The temperature range to set.

            Raises:
                TypeError: If the provided value is not an instance of WaterPropertyRange.
        """
        if not isinstance(value, WaterPropertyRange):
            raise TypeError("Temperature Range must be an instance of WaterPropertyRange")
        self._temperature_range=value

    @property
    def tds_range(self)->WaterPropertyRange:
        """
        Get the TDS (Total Dissolved Solids) range property.

            Returns:
                WaterPropertyRange: The range of TDS values.
        """
        return self._tds_range

    @tds_range.setter
    def tds_range(self, value: WaterPropertyRange):
        """
        Set the TDS range for the water property.

            Args:
                value (WaterPropertyRange): The TDS range to set.

            Raises:
                TypeError: If the provided value is not an instance of WaterPropertyRange.
        """
        if not isinstance(value, WaterPropertyRange):
            raise TypeError("TDS Range must be an instance of WaterPropertyRange")
        self._tds_range=value

    @property
    def alerts(self)->list:
        """
        Get the list of alerts generated during analysis.

            Returns:
                list: List of alert messages.
        """
        return self._alerts

    @alerts.setter
    def alerts(self, value: str):

        """
        Set the alerts property with a new alert value.

            Args:
                value (str): The alert message to be added.

            Raises:
                TypeError: If the provided value is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("Alert must be a string.")
        self._alerts.append(value)

    @property
    def status(self) -> dict:
        """
        Get the status property.

            Returns:
                dict: The current status as a dictionary.
        """
        return self._status

    @status.setter
    def status(self, value: dict):
        """
        Set the status property with a new status value.

            Args:
                value (dict): The new status to set.

            Raises:
                TypeError: If the provided value is not a dictionary.
        """
        if not isinstance(value, dict):
            raise TypeError("Status must be a dictionary.")
        self._status.update(value)

    def validate_data(self, water_data: dict) -> bool:
        """
        Validate water data against expected properties and types.

                Args:
                    water_data (dict): A dictionary containing water properties and their values.

                Returns:
                    bool: True if all data is valid.

                Raises:
                    TypeError: If any value in water_data is not numeric.
                    AttributeError: If a water property does not have a corresponding range attribute in the class.
        """
        for water_property, value in water_data.items():
            if not isinstance(value, (float, int)):
                raise TypeError(f"Value for {water_property} must be numeric.")
            elif not hasattr(self,f"{water_property}_range"):
                raise AttributeError(f"No attribute found for {water_property}.")
        return True

    def analyze_data(self, water_data: dict) -> bool:
        """
        Analyze water data against predefined acceptable ranges for each property.

            Args:
                water_data (dict): A dictionary containing water properties and their corresponding values.

            Returns:
                bool: True if all water properties are within acceptable ranges, False otherwise.

            Side Effects:
                Updates the `status` attribute with the analysis result for each water property.
                Calls `generate_alert` method if any property is outside the acceptable range.
        """
        for water_property, value in water_data.items():
            property_range=getattr(self,f"{water_property}_range")
            if not (property_range.lower_bound<=value<=property_range.upper_bound):
                self.status = {water_property:f"{value} is outside the acceptable range."}
                self.generate_alert(water_property,value)
            else:
                self.status = {water_property: "OK"}

        if any(status != "OK" for status in self.status.values()):
                return False
        return True

    def generate_alert(self, parameters: str, value: float|int):
        """
        Generate and log an alert message when a parameter value is out of range.

                Args:
                    parameters (str): The name of the parameter that is out of range.
                    value (float|int): The value of the parameter that is out of range.

                Returns:
                    str: The generated alert message.

                Side Effects:
                    Appends the alert message to the `alerts` list and prints it to the console.
        """
        msg_alert = f"Alert! {parameters}: {value} out of range"
        self.alerts = msg_alert
        return msg_alert

    def clean_alerts(self):
        """
        Clears the alerts list.
        """
        self.alerts.clear()

    def output_status(self):
        """
        Returns the current status of the object.

            Returns:
                The status attribute of the object.
        """
        return self.status
