from src.simulation.water.water_property_range import WaterPropertyRange
from src.simulation.water.water_tank import WaterTank
from functools import wraps


class WaterDissolvedElementsMonitor:
    def __init__(self, water_tank: WaterTank, dissolved_elements: dict):
        if not isinstance(water_tank, WaterTank):
            raise TypeError("The `water_tank` parameter must be a `WaterTank` instance.")
        self.water_tank = water_tank
        self._set_dissolved_elements(dissolved_elements)

        # Track the initial volume of the water to handle proportional updates
        self._last_known_volume = self.water_tank.current_volume

        # Decorate the Water instance's `evaporate` method
        self._decorate_evaporate_method()

        # Decorate the Water instance's `manage_precipitation` method
        self._decorate_manage_precipitation()

        # Decorate the Water instance's `add_water` method
        self._decorate_add_water()

    def _get_dissolved_element_properties(self):
        """
        Retrieves all properties of the WaterDissolvedElementsMonitor instance that represent
        dissolved element concentrations. These are attributes that do not contain "_range".
        """
        if not hasattr(self, "_cached_dissolved_properties"):
            self._cached_dissolved_properties = [
                attr.removeprefix('_').removesuffix('_dissolved_element')
                for attr in self.__dict__.keys()
                if not attr.endswith("_range") and attr.endswith("_dissolved_element")
            ]
        return self._cached_dissolved_properties

    def _decorate_evaporate_method(self):
        """
        Decorates the evaporate method of the Water instance within the WaterTank
        to automatically adjust dissolved element concentrations after evaporation.
        """
        if not hasattr(self.water_tank, 'evaporate'):
            raise AttributeError(f"The method 'evaporate' does not exist in WaterTank.")

        original_evaporate = self.water_tank.evaporate  # Store the original evaporate method

        @wraps(original_evaporate)  # Preserve metadata of the original method
        def evaporate_with_concentration_update(*args, **kwargs):
            # Call the original evaporate method and get the amount evaporated
            evaporated_water = original_evaporate(*args, **kwargs)

            # Adjust the dissolved element concentrations
            new_volume = self.water_tank.current_volume

            # Handle edge cases (no volume left or no evaporation occurred)
            if new_volume <= 0:
                # Set all element concentrations to 0 if no water remains
                for element in self._get_dissolved_element_properties():
                    setattr(self, element, 0)
            else:
                # Update concentrations based on volume reduction
                for element in self._get_dissolved_element_properties():
                    # Calculate updated concentration
                    current_concentration = getattr(self, element)
                    concentration_increment = current_concentration * (1 - (new_volume / self._last_known_volume))
                    new_concentration = current_concentration + concentration_increment
                    setattr(self, element, new_concentration)

            # Update the tracked volume
            self._last_known_volume = new_volume

            return evaporated_water  # Return the result from the original method

        # Replace the original evaporate method with the decorated one
        self.water_tank.evaporate = evaporate_with_concentration_update

    def _decorate_manage_precipitation(self):
        """
        Decorates the manage_precipitation method of the WaterTank instance 
        to update dissolved element concentrations automatically whenever 
        precipitation occurs, incorporating water volume changes.
    
        This ensures that the concentrations of dissolved elements in the water 
        are recalculated in proportion to the updated water volume after precipitation.
    
        Inputs:
            - *args, **kwargs: Any arguments passed to the original manage_precipitation method.
        Outputs:
            - The decorated method does not modify the return value of the original method.
        """
        if not hasattr(self.water_tank, 'manage_precipitation'):
            raise AttributeError(f"The method 'manage_precipitation' does not exist in WaterTank.")

        # Store the original manage_precipitation method
        original_manage_precipitation = self.water_tank.manage_precipitation
    
        # Preserve metadata of the original method
        wraps(original_manage_precipitation)
    
        # Define the wrapped method
        def manage_precipitation_with_dissolved_elements_concentration_update(*args, **kwargs):
            # Call the original manage_precipitation method
            original_manage_precipitation(*args, **kwargs)
    
            # Loop through each dissolved element to update its concentration
            for element in self._get_dissolved_element_properties():
                # Get the current concentration level
                current_concentration = getattr(self, element)
    
                # Calculate the change in concentration due to precipitation
                concentration_decrement = current_concentration * (1 - (self.water_tank.current_volume / self._last_known_volume))
    
                # Apply the calculated changes to update the concentration
                new_concentration = current_concentration + concentration_decrement
    
                # Set the new concentration value
                setattr(self, element, new_concentration)
    
        # Replace the original manage_precipitation method with the decorated version
        self.water_tank.manage_precipitation = manage_precipitation_with_dissolved_elements_concentration_update

    def _decorate_add_water(self):
        """
        Decorates the `add_water` method of the WaterTank instance 
        to adjust dissolved element concentrations automatically 
        whenever water is added, maintaining consistency with the 
        proportional change in water volume.
        """
        if not hasattr(self.water_tank, 'add_water'):
            raise AttributeError(f"The method 'add_water' does not exist in WaterTank.")
        
        # Store the original `add_water` method from WaterTank
        original_add_water = self.water_tank.add_water
        
        # Preserve the original method's metadata
        wraps(original_add_water)
    
        # Define the decorated method
        def add_water_with_dissolved_elements_concentration_update(*args, **kwargs):
            # Call the original `add_water` method
            original_add_water(*args, **kwargs)
            
            # Adjust each dissolved element's concentration based on the new volume
            for element in self._get_dissolved_element_properties():
                current_concentration = getattr(self, element)
                
                # Calculate the decrease in concentration proportional to added water volume
                concentration_decrement = current_concentration * (1 - (self.water_tank.current_volume / self._last_known_volume))
                
                # Update the concentration
                new_concentration = current_concentration + concentration_decrement
                setattr(self, element, new_concentration)
    
        # Replace the original `add_water` method with the new decorated one
        self.water_tank.add_water = add_water_with_dissolved_elements_concentration_update

    def _set_dissolved_elements(self, dissolved_elements: dict):
        """
        Dynamically sets dissolved element properties and their ranges for the water tank.

        Args:
            dissolved_elements (dict): A dictionary where each key is the name of an element (str),
                                       and each value is another dictionary with the following keys:
                                       - 'initial' (float): The initial concentration of the element.
                                       - 'min' (float): The minimum acceptable concentration of the element.
                                       - 'max' (float): The maximum acceptable concentration of the element.

        Raises:
            ValueError: If 'min' is greater than 'max' for any element.
            TypeError: If any concentration or range value is not numeric.
        """
        if not isinstance(dissolved_elements, dict):
            raise TypeError("The dissolved_elements parameter must be a dictionary.")

        if not dissolved_elements:
            raise ValueError("The dissolved_elements dictionary cannot be empty.")

        for element, element_dict in dissolved_elements.items():
            # Update class dictionary WaterPropertyRange.properties_ranges
            WaterPropertyRange.properties_ranges[element] = {"lower_bound": element_dict['min'],
                                                             "upper_bound": element_dict['max']}
            def create_value_getter(e):  # Capture loop variable
                def value_getter(class_instance):
                    return class_instance.__dict__.get(f"_{e}_dissolved_element", 0)

                return value_getter

            def create_value_setter(e):
                def value_setter(class_instance, value):
                    if not isinstance(value, (int, float)):
                        raise TypeError(f"{e} concentration must be a numeric value.")
                    elif value < 0:
                        raise ValueError(f"{e} concentration must be non-negative.")
                    value_range = class_instance.__dict__.get(f"_{e}_range", None)
                    if value_range is not None:
                        value_range.check_property_value(value)
                    class_instance.__dict__[f"_{e}_dissolved_element"] = value

                return value_setter

            def create_range_getter(e):
                def range_getter(class_instance):
                    return class_instance.__dict__.get(f"_{e}_range", None)

                return range_getter

            def create_range_setter(e):
                def range_setter(class_instance, range_value):
                    if not isinstance(range_value, WaterPropertyRange):
                        raise TypeError(f"{e} range must be a WaterPropertyRange object.")
                    if range_value.property_name != e:
                        raise ValueError(f"{e} range must match the corresponding element.")
                    class_instance.__dict__[f"_{e}_range"] = range_value

                return range_setter

            # Validate and initialize values
            min_value = element_dict.get("min", 0)
            max_value = element_dict.get("max", 0)
            initial_value = element_dict.get("initial", 0)

            if not isinstance(min_value, (int, float)) or not isinstance(max_value, (int, float)):
                raise TypeError(f"Element '{element}' must have numeric 'min' and 'max' values.")

            if min_value > max_value:
                raise ValueError(f"Element '{element}' has 'min' greater than 'max'.")

            # Create WaterPropertyRange object
            element_range = WaterPropertyRange(element, min_value, max_value)

            # Assign dynamic properties
            setattr(self.__class__, element, property(
                fget=create_value_getter(element),
                fset=create_value_setter(element)
            ))
            setattr(self.__class__, f"{element}_range", property(
                fget=create_range_getter(element),
                fset=create_range_setter(element)
            ))

            # Use the dynamically defined property setters to initialize values
            setattr(self, f"{element}_range", element_range)
            setattr(self, element, initial_value)

