# src/simulation/water/water.py
import math
from src.simulation.water.water_property_range import WaterPropertyRange

class Water:
    def __init__(self, initial_nutrients, tank_capacity):
        self.nutrients = initial_nutrients
        self.tank_capacity = tank_capacity
        self.current_nutrients = initial_nutrients
        self._current_volume = 0  # Initialize current volume
        self.overflow_volume = 0
        self._underflow_capacity_threshold = 0.2
        self._overflow_capacity_threshold = 0.1
        self.snow_accumulation = 0  # Initialize snow accumulation
        self._temperature = 25  # Default temperature in Celsius
        self._ph = 7.0  # Neutral pH
        self._turbidity = 0  # Clear water
        self._viscosity = 0.00089  # Default viscosity of pure water at 25 degrees C
        self._tds = 0  # Default TDS value
        self.is_empty = True
        self.is_full = False

    @property
    def temperature(self):
        """
        Get the current temperature of the water.

        This property returns the temperature value, expressed in degrees Celsius.
        The temperature of the water affects various properties and behaviors,
        such as snow melting in precipitation management and evaporation rates.
        It is constrained to typical physical bounds (e.g., 0-100°C) in the class
        via its setter method.

        Returns:
            float: The current temperature of the water in degrees Celsius.
        """
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        """
        Setter for the `temperature` property that assigns a value to the private `_temperature` attribute.

        Validates that the provided temperature is within an acceptable range (0 to 100 degrees Celsius).
        If the value falls outside this range, it raises a `ValueError`.
        
        Updates the `viscosity` attribute based on the new temperature value.

        Parameters:
            value (int | float): The temperature value to set (must be between 0 and 100).

        Raises:
            ValueError: If the temperature is not within the range of 0 to 100 degrees Celsius.
            TypeError: If the provided value is not a numeric type (int or float).
        """
        if not (0 <= value <= 100):
            raise ValueError("Temperature must be between 0 and 100 degrees Celsius.")
        elif not isinstance(value, (int, float)):
            raise TypeError("Temperature must be a numeric value.")
        self._temperature = value
        self.update_water_viscosity()

    @property
    def ph(self):
        """
        Get the pH level of the water.

        The pH level is a measure of how acidic or basic the water is,
        with values ranging from 0 (very acidic) to 14 (very basic). A
        typical default value for pH in this context is 7.0, representing
        neutral water.

        Returns:
            float: The current pH level of the water.
        """
        return self._ph

    @ph.setter
    def ph(self, value):
        """
        Sets the value of the pH level of the water.

        Validates that the pH value is within the permissible range of 0 to 14.
        If the value is outside this range, a ValueError is raised.

        Parameters:
            value (int | float): The desired pH level to set. Must be between 0 and 14.

        Raises:
            ValueError: If the provided pH value is not within the range of 0 to 14.
            TypeError: If the provided value is not a numeric type (int or float).
        """
        if not (0 <= value <= 14):
            raise ValueError("pH must be between 0 and 14.")
        if not isinstance(value, (int, float)):
            raise TypeError("pH must be a numeric value.")
        self._ph = value

    @property
    def turbidity(self):
        """
        Represents the turbidity level of the water.

        Turbidity refers to the cloudiness or haziness of a liquid caused by large numbers
        of individual particles. It is typically measured in NTU (Nephelometric Turbidity Units).

        Returns:
            int or float: The current turbidity value of the water. The value must fall within
            the valid range defined in the application (e.g., 0 to 1000).
        """
        return self._turbidity

    @turbidity.setter
    def turbidity(self, value):
        """
        Sets the turbidity of the water.

        The turbidity represents the cloudiness or haziness of the water, which is
        typically measured in NTU (Nephelometric Turbidity Units). This setter
        ensures that the turbidity value is not negative, as turbidity values
        below zero are invalid.

        Args:
            value (float | int): The turbidity value to set. Must be greater than or equal to 0.

        Raises:
            ValueError: If the turbidity value is negative.
            TypeError: If the provided value is not a numeric type (int or float).
        """
        if value < 0:
            raise ValueError("Turbidity cannot be negative.")
        elif not isinstance(value, (int, float)):
            raise TypeError("Turbidity must be a numeric value.")
        self._turbidity = value

    @property
    def viscosity(self):
        """
        Retrieve the current viscosity of the water.

        Viscosity is a measure of the water's resistance to flow, which can be influenced by
        various factors such as temperature and the presence of dissolved substances.
        This property stores the current viscosity value, which is typically positive.

        Returns:
            float: The current viscosity of the water.
        """
        return self._viscosity

    @viscosity.setter
    def viscosity(self, value):
        """
        Sets the viscosity value for the Water object.

        This method ensures that the input is a valid positive numeric value
        as viscosity cannot be negative or zero. It raises an exception if
        the input value violates the constraints.

        Args:
            value (int | float): The new viscosity value to be set.

        Raises:
            ValueError: If the viscosity value is non-positive (<= 0).
            TypeError: If the viscosity value is not a numeric type (int or float).

        Example:
            water = Water(50, 100)
            water.viscosity = 1.0  # Valid
            water.viscosity = 0    # Raises ValueError
            water.viscosity = "a"  # Raises TypeError
        """
        if value <= 0:
            raise ValueError("Viscosity must be positive and non-zero.")
        elif not isinstance(value, (int, float)):
            raise TypeError("Viscosity must be a numeric value.")
        self._viscosity = value

    @property
    def tds(self):
        """
        Get the current Total Dissolved Solids (TDS) of the water.

        This property represents the concentration of dissolved substances
        (e.g., minerals, salts, and organic matter) in the water, measured in ppm (parts per million).
        """
        return self._tds

    @tds.setter
    def tds(self, value):
        """
        Setter method for the Total Dissolved Solids (TDS) attribute.

        This method sets the TDS value for the water instance. TDS represents
        the concentration of dissolved solids in the water, measured in units
        like ppm (parts per million).
        
        Updates the `viscosity` attribute based on the new TDS value.

        Validations:
        - The TDS value must be numeric (either an integer or a float).
        - The TDS value cannot be negative.

        Args:
            value (int | float): The new TDS value to be set.

        Raises:
            ValueError: If the provided TDS value is negative.
            TypeError: If the provided TDS value is not numeric.
        """
        if value < 0:
            raise ValueError("TDS cannot be negative.")
        elif not isinstance(value, (int, float)):
            raise TypeError("TDS must be a numeric value.")
        self._tds = value
        self.update_water_viscosity()
    
    @property
    def current_volume(self) -> int|float:
        """
        Get the current water volume in the tank.
    
        This property represents the current volume of water in the system, measured in liters.
        Ensures that water volume is non-negative and within the tank's capacity.
        
        Returns:
            int | float: The current water volume in liters.
        """
        return self._current_volume
    
    @current_volume.setter
    def current_volume(self, value: int|float):
        """
        Set the current volume of water in the tank.
    
        This setter assigns a value to the water volume, ensuring it is a valid numeric value,
        non-negative, and does not exceed the tank's total capacity. If the provided volume exceeds
        the tank's capacity, it calculates the overflow and caps the volume at the maximum capacity.
    
        Parameters:
            value (int | float): The water volume to set, measured in liters.
    
        Raises:
            TypeError: If the provided value is not of a numeric type (int or float).
            ValueError: If the value is negative or exceeds the tank's total capacity.
    
        Notes:
            - The overflow amount is calculated and assigned to `overflow_volume` when the input value
              exceeds the tank's capacity.
            - In case of overflow, the water volume is limited to the tank's capacity.
        """
        # Ensure the provided value is numeric
        if not isinstance(value, (int, float)):
            raise TypeError("Current volume must be a numeric value.")
        
        # Check that the volume is non-negative
        if value < 0:
            raise ValueError("Current volume must be non-negative.")
    
        # If the volume exceeds the tank capacity, calculate overflow
        if value > self.tank_capacity:
            self.overflow_volume = value - self.tank_capacity  # Calculate overflow
            self._current_volume = self.tank_capacity  # Cap the volume at tank capacity
            raise ValueError("Current volume cannot exceed the tank's capacity.")

        # Otherwise, update the current volume directly
        else:
            self._current_volume = value  # Assign the validated volume

        if self.current_volume <= self.underflow_capacity_threshold:
            self.is_empty = True
        else:
            self.is_empty = False

        if self.current_volume >= self.tank_capacity - self.overflow_capacity_threshold:
            self.is_full = True
        else:
            self.is_full = False
    
    @property
    def underflow_capacity_threshold(self) -> int | float:
        """
        Get the current underflow capacity threshold of the water system.
    
        The underflow threshold is calculated as a fraction of the tank's capacity,
        representing the minimum water level that should be maintained in the tank.
        If the water volume falls below this threshold, it may trigger an underflow alert.
    
        Returns:
            int | float: The underflow threshold, in liters, as a fraction of the tank's total capacity.
        """
        return self.tank_capacity * self._underflow_capacity_threshold
    
    @underflow_capacity_threshold.setter
    def underflow_capacity_threshold(self, value: int | float):
        """
        Set the underflow capacity threshold.
    
        This property defines the minimum water level needed to avoid underflow, relative to the 
        tank's capacity. Two approaches are supported for setting the threshold:
        - If the input value is <= 1, it is treated as a fraction of the total capacity.
        - If the input value is > 1, it is assumed to be an absolute volume in liters, which will 
          be converted to a fraction of the tank's capacity.
    
        The setter ensures that the threshold does not exceed the tank capacity limits and is
        positive. Providing a value >= the tank capacity or less than 0 triggers a `ValueError`.
    
        Parameters:
            value (int | float): The numeric underflow threshold to set. 
    
        Raises:
            ValueError: If the threshold is less than 0, invalid, or exceeds the tank's total capacity.
            TypeError: If the provided value is not a numeric type.
        """
        # Validation: Ensure the value is non-negative
        if value < 0:
            raise ValueError("Underflow threshold cannot be negative.")
        # Validation: Ensure the value is numeric
        elif not isinstance(value, (int, float)):
            raise ValueError("Underflow threshold must be a numeric value.")
        # If value is greater than 1, treat it as an absolute volume in liters
        elif value > 1:
            if value >= self.tank_capacity - self.overflow_capacity_threshold:
                raise ValueError("Underflow threshold must be less than or equal to the tank capacity.")
            self._underflow_capacity_threshold = value / self.tank_capacity
        # If value is a fraction, assign it as is
        elif value >= 0:
            self._underflow_capacity_threshold = value

    @property
    def overflow_capacity_threshold(self) -> int | float:
        """
        Retrieve the overflow capacity threshold of the tank.

        The overflow threshold is calculated as a fraction of the tank's total capacity.
        It represents the maximum limit of water volume that the tank can hold without spilling over.
        Any volume added beyond this threshold will result in overflow.

        Returns:
            int | float: The overflow threshold, in liters, as a fraction of the tank's total capacity.
        """
        return self.tank_capacity * self._overflow_capacity_threshold

    @overflow_capacity_threshold.setter
    def overflow_capacity_threshold(self, value: int | float):
        """
        Set the overflow capacity threshold of the tank.
        
        This setter allows configuring the overflow limit as either a fraction of the tank's total 
        capacity or an absolute volume in liters:
        - If the input value is <= 1, it is treated as a fraction of the total capacity.
        - If the input value is > 1, it is assumed to be an absolute volume, which will be converted 
          to a fraction relative to the tank's total capacity.
        
        The setter ensures that the threshold is non-negative and does not exceed the tank's total 
        capacity. If the threshold exceeds the defined tank capacity, a `ValueError` is raised.
        
        Args:
            value (int | float): The desired overflow threshold to set, in either fractional or 
                                 absolute terms.
        
        Raises:
            ValueError: If the threshold is negative or exceeds the tank's total capacity.
            TypeError: If the input value is not of a numeric type (int or float).
        """
        # Check that the input value is non-negative
        if value < 0:
            raise ValueError("Overflow threshold cannot be negative.")
        # Validate input type as numeric
        elif not isinstance(value, (int, float)):
            raise TypeError("Overflow threshold must be a numeric value.")
        # If value is greater than or equal to 1, treat it as an absolute volume
        elif value >= 1:
            if value >= self.tank_capacity:
                raise ValueError("Overflow threshold must be less than the tank capacity.")
            self._overflow_capacity_threshold = value / self.tank_capacity
        # If value is a fraction, directly assign it
        elif value >= 0:
            self._overflow_capacity_threshold = value

    @property
    def status(self) -> dict:
        """
        Retrieve the current status of the water system.
    
        This property compiles a dictionary containing various attributes and metrics associated with the current state of the water system.
        The dictionary includes physical properties (e.g., temperature, pH, turbidity, viscosity, and TDS), capacity states (e.g., current volume,
        underflow and overflow thresholds, and whether the system is empty or full), and tank-related metrics (e.g., capacity and overflow volume).
    
        Returns:
            dict: A dictionary summarizing the current status of the water system.
        """
        return {
            "temperature": self.temperature,
            "ph": self.ph,
            "turbidity": self.turbidity,
            "viscosity": self.viscosity,
            "tds": self.tds,
            "current_volume": self.current_volume,
            "underflow_capacity_threshold": self.underflow_capacity_threshold,
            "overflow_capacity_threshold": self.overflow_capacity_threshold,
            "is_empty": self.is_empty,
            "is_full": self.is_full,
            "tank_capacity": self.tank_capacity,
            "overflow_volume": self.overflow_volume
        }

    def update_water_viscosity(self):
        """
        Update the viscosity of the water based on temperature and TDS (Total Dissolved Solids).

        This improved version calculates water viscosity using a more precise empirical formula for the
        temperature dependence and a nonlinear approximation for the TDS effect.

        Effects:
            - Updates `self.viscosity` based on the calculated value.

        Formula for temperature-based viscosity:
            η(T) = A * e^(B / (T_kelvin - C))
              - A: Empirical constant (viscosity factor for water)
              - B: Empirical constant (activation energy term for water viscosity)
              - C: Empirical constant (accounts for anomaly in water viscosity behavior)
              - T_kelvin: The water temperature in Kelvin (°C + 273.15)

        Formula for TDS effect:
            viscosity_with_tds = base_viscosity * (1 + k_tds * self.tds^n)
              - k_tds: Coefficient for sensitivity of viscosity to TDS increase.
              - n: Exponent to model the nonlinear relationship (e.g., exponential or polynomial).

        Threshold:
            - Ensures viscosity never drops below a small positive value (e.g., 0.1).

        Constants:
            - A, B, C: Temperature-specific constants for water viscosity.
            - k_tds: Coefficient to model TDS impact on viscosity.
            - n: Exponent to adjust the weight of TDS impact.

        Returns:
            None
        """
        # Constants for temperature-based viscosity (empirically determined for water)
        A = 8.569944981455998e+155  # Empirical scaling for water viscosity (Pa·s)
        B = 8101783.244249629  # Temperature sensitivity constant
        C = 22428.609592644887  # Offset constant for water temperature behavior

        # Constants for TDS impact
        k_tds = 0.001  # Coefficient for TDS contribution to viscosity
        n = 0.5  # Exponent for TDS effect (adjust to make nonlinear)

        # Convert temperature to Kelvin
        temperature_kelvin = self.temperature + 273.15

        # Calculate base viscosity using empirical temperature formula
        base_viscosity = A * math.exp(B / (temperature_kelvin - C))

        # Adjust viscosity based on TDS
        viscosity_with_tds = base_viscosity * (1 + k_tds * math.pow(self.tds, n))
        viscosity_with_tds = round(viscosity_with_tds, 5)

        # Ensure viscosity never goes below a realistic minimum threshold (0.000282) pure water at 100 degrees C
        self.viscosity = max(viscosity_with_tds, 0.000282)

    def manage_precipitation(self, precipitation_type: str, amount: int, pattern: str = 'steady'):
        """
        Manages the effect of precipitation (rain or snow) on the water system.

        This method adjusts the current water volume based on the precipitation type,
        amount, and other environmental factors like temperature, which impacts snow melting.
        Rain directly increases the water volume, while snow accumulates and melts
        depending on the temperature.

        Parameters:
            precipitation_type (str): The type of precipitation ('rain' or 'snow').
            amount (float): The amount of precipitation received (in liters or appropriate unit).
            pattern (str): The pattern of precipitation (e.g., 'steady', 'intermittent').
                           [Note: Currently unused, provided for potential future use.]

        Raises:
            ValueError: If precipitation_type is not 'rain' or 'snow'.

        Notes:
            - Snow melting is simulated by assuming snow melts at a rate corresponding to
              the temperature, provided the temperature is above 0°C.
        """
        # Validate precipitation type
        if precipitation_type not in ['rain', 'snow']:
            raise ValueError("Invalid precipitation type. Must be 'rain' or 'snow'.")
        elif not isinstance(precipitation_type, str):
            raise TypeError("Precipitation type must be a string.")

        # Validate amount
        if not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a numeric value.")
        elif amount < 0:
            raise ValueError("Amount must be non-negative.")

        # Validate pattern
        if pattern not in ['steady', 'intermittent']:
            raise ValueError("Invalid pattern. Must be 'steady' or 'intermittent'.")
        elif not isinstance(pattern, str):
            raise TypeError("Pattern must be a string.")

        # Handle rain: directly add the amount to the current water volume
        if precipitation_type == 'rain' and pattern == 'steady':
            self.current_volume += amount
        elif precipitation_type == 'rain' and pattern == 'intermittent':
            self.current_volume += amount * 0.5

        # Handle snow: accumulate and consider melting based on temperature
        elif precipitation_type == 'snow':
            # Snow accumulates in a separate variable
            self.snow_accumulation += amount

            # Simulate snow melting if temperature is above 0°C
            if self.temperature > 0:  # Snow melts at temperatures greater than 0°C
                # Determine the amount of snow that melts
                melting_rate = int(self.temperature ** 2)  # Quadratic relation
                melted_snow = min(self.snow_accumulation, melting_rate)

                # Add the melted snow to the current water volume
                self.current_volume += melted_snow

                # Subtract the melted snow from the remaining snow accumulation
                self.snow_accumulation -= melted_snow

    def evaporate(self,
                  air_temp: int | float,
                  surface_area: int | float,
                  rel_humidity: int | float,
                  time_elapsed_sec: int) -> int | float:
        """
        Calculate the amount of water evaporated over a given time period.

        This method estimates the amount of water evaporated, in liters, based on
        air temperature, surface area, relative humidity, and elapsed time. It uses
        the Antoine equation to calculate the vapor pressure of water and factors
        in external environmental conditions to determine the evaporation rate.
        After the amount of water evaporated is calculated, the method updates the current_volume attribute.

        Parameters:
            air_temp (int | float): The air temperature in degrees Celsius.
                                    Must be between -10 and 50.
            surface_area (int | float): The surface area of the water exposed to air, in square meters.
                                         Must be between 1 and 100.
            rel_humidity (int | float): The relative humidity of the surrounding air, as a percentage.
                                        Must be between 0 and 100.
            time_elapsed_sec (int): The total time elapsed for evaporation, in seconds.

        Returns:
            int | float: The total amount of water evaporated, in liters.

        Raises:
            TypeError: If any input parameter is not numeric.
            ValueError: If any input parameter is outside the acceptable range.
        """
        # Validate that air_temp is a numeric value and within the acceptable range (-10 to 50 degrees Celsius)
        if not isinstance(air_temp, (int, float)):
            raise TypeError("Air temperature must be a numeric value.")
        air_temp_range = WaterPropertyRange("temperature", -10, 50)
        if air_temp_range.lower_bound > air_temp or air_temp_range.upper_bound < air_temp:
            raise ValueError(f"Air temperature must be between {air_temp_range.lower_bound} "
                             f"and {air_temp_range.upper_bound} degrees Celsius.")

        # Validate that surface_area is numeric and within the acceptable range (1 to 100 square meters)
        if not isinstance(surface_area, (int, float)):
            raise TypeError("Surface area must be a numeric value.")
        surface_are_range = WaterPropertyRange("surface_area", 0, 100)
        if surface_are_range.lower_bound > surface_area or surface_are_range.upper_bound < surface_area:
            raise ValueError(f"Surface area must be between {surface_are_range.lower_bound} "
                             f"and {surface_are_range.upper_bound} square meters.")
        # When there is no water surface exposed to ambient air there is no evaporation
        if surface_area == 0:
            return 0

        # Validate that rel_humidity is numeric and within the range (0 to 100 percent)
        if not isinstance(rel_humidity, (int, float)):
            raise TypeError("Relative humidity must be a numeric value.")
        rel_humidity_range = WaterPropertyRange("relative_humidity", 0, 100)
        if rel_humidity_range.lower_bound > rel_humidity or rel_humidity_range.upper_bound < rel_humidity:
            raise ValueError(f"Relative humidity must be between {rel_humidity_range.lower_bound} "
                             f"and {rel_humidity_range.upper_bound} percent.")

        # Validate that time_elapsed_sec is a numeric value
        if not isinstance(time_elapsed_sec, (int, float)):
            raise TypeError("Time must be a numeric value.")

        # Constants for the Antoine equation for water (used for calculating vapor pressure)
        a_const = 8.07131
        b_const = 1730.63
        c_const = 233.426

        # Calculate the saturation vapor pressure (SVP) of water using the Antoine equation
        # SVP is the maximum pressure exerted by water vapor at the current water temperature
        saturation_vapor_pressure = 10 ** (a_const - (b_const / (c_const + self.temperature)))

        # Calculate the actual vapor pressure (AVP) of air using relative humidity
        # AVP accounts for the water vapor already present in the air
        saturation_vapor_pressor_air = rel_humidity * saturation_vapor_pressure

        # Evaporation rate coefficient (k) varies depending on air temperature relative to water temperature
        k = 0.1 + 0.01 * (air_temp - self.temperature)

        # Calculate the evaporation rate in grams per hour
        # This is determined by the difference between SVP and AVP, the surface area, and the coefficient
        evaporation_rate = k * surface_area * (saturation_vapor_pressure - saturation_vapor_pressor_air)

        # Convert the elapsed time from seconds to hours (as evaporation rate is in grams/hour)
        time_elapsed_hours = time_elapsed_sec / 3600

        # Calculate total water evaporated in grams over the given time period
        total_evaporation_grams = evaporation_rate * time_elapsed_hours

        # Convert the total evaporation from grams to liters (1 liter = 1000 grams)
        total_evaporation_liters = total_evaporation_grams / 1000

        # Update current_volume property by removing the evaporated water volume
        self.current_volume -= total_evaporation_liters

        # Return the total evaporation in liters
        return total_evaporation_liters

    def add_water(self, amount: int | float) -> int | float:
        """
        Add a specified amount of water to the tank.
    
        This method increases the current water volume by the given `amount`,
        provided it does not exceed the tank's capacity or violate any constraints.
    
        Parameters:
            amount (int | float): The amount of water to add, in liters. Must be 
                                  a positive numeric value.
    
        Returns:
            int | float: The amount of water successfully added to the tank.
    
        Raises:
            ValueError: If the amount is not positive, exceeds the tank's total 
                        capacity, or causes overflow beyond the acceptable range.
            TypeError: If the provided amount is not numeric.
        """
        # Check if the provided amount is non-negative and greater than zero
        if amount <= 0:
            raise ValueError("Amount must be non-negative and greater than zero.")
        
        # Validate the type of the provided amount
        elif not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a numeric value.")
        
        # Ensure the amount does not exceed the overall tank capacity
        elif amount > self.tank_capacity:
            raise ValueError(f"Amount must be less than or equal to the tank capacity {self.tank_capacity} liters.")
        
        # Check if the addition of the amount exceeds the remaining capacity of the tank
        elif amount > self.tank_capacity - self.current_volume:
            raise ValueError("Amount exceed the tank capacity when added to current volume.")
        
        # If all checks pass, add the specified amount to the current water volume
        else:
            self.current_volume += amount
            return amount

    def extract_water(self, amount: int | float, force_underflow_capacity_threshold: bool = False) -> int | float:
        """
        Extract a specified amount of water from the tank.
    
        This method reduces the current water volume by the specified `amount`, provided it
        does not breach the underflow capacity threshold. The `force_underflow_capacity_threshold`
        parameter can be set to override the underflow constraint.
    
        Parameters:
            amount (int | float): The amount of water to be extracted, in liters.
                                  Must be a non-negative value and not exceed the current volume.
            force_underflow_capacity_threshold (bool): If True, allows extraction below the 
                                                       underflow threshold. Defaults to False.
    
        Returns:
            int | float: The actual amount of water extracted from the tank.
    
        Raises:
            ValueError: If the `amount` is negative, exceeds the current volume, or is invalid
                        relative to the underflow threshold.
            TypeError: If the `amount` is not a numeric value.
        """
        # Ensure the extraction amount is non-negative
        if amount < 0:
            raise ValueError("Amount must be non-negative.")
    
        # Validate that the extraction amount is numeric
        elif not isinstance(amount, (int, float)):
            raise TypeError("Amount must be a numeric value.")
    
        # Check if extraction violates the underflow threshold unless force is enabled
        elif amount > self.current_volume - self.underflow_capacity_threshold and not force_underflow_capacity_threshold:
            raise ValueError("Amount must be less than or equal to the current volume minus the underflow threshold.")
    
        # Ensure the amount does not exceed the current volume
        elif amount > self.current_volume:
            raise ValueError("Amount must be less than or equal to the current volume.")
    
        # Proceed with extraction if all checks pass
        else:
            self.current_volume -= amount  # Reduce the current volume
            return amount  # Return the amount of water extracted
