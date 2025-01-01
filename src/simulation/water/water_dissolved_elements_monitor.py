from src.simulation.water.water_property_range import WaterPropertyRange
from src.simulation.water.water_tank import WaterTank
from functools import wraps


class WaterDissolvedElementsMonitor:
    def __init__(self, water_tank: WaterTank, dissolved_elements: dict):
        if not isinstance(water_tank, WaterTank):
            raise TypeError("The `water_tank` parameter must be a `WaterTank` instance.")
        self.water_tank = water_tank
        self.set_dissolved_elements(dissolved_elements)

        # Track the initial volume of the water to handle proportional updates
        self._last_known_volume = self.water_tank.current_volume

        # Decorate the Water instance's `evaporate` method
        self.decorate_evaporate_method()

    def _get_dissolved_element_properties(self):
        """
        Retrieves all properties of the WaterDissolvedElementsMonitor instance that represent
        dissolved element concentrations. These are attributes that do not contain "_range".
        """
        return [
            attr.removeprefix('_').removesuffix('_dissolved_element')
            for attr in self.__dict__.keys()
            if not attr.endswith("_range") and attr.endswith("_dissolved_element")
        ]

    def decorate_evaporate_method(self):
        """
        Decorates the evaporate method of the Water instance within the WaterTank
        to automatically adjust dissolved element concentrations after evaporation.
        """
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
                    concentration_reduction = current_concentration * (1 - (new_volume / self._last_known_volume))
                    new_concentration = max(0, current_concentration - concentration_reduction)
                    setattr(self, element, new_concentration)

            # Update the tracked volume
            self._last_known_volume = new_volume

            return evaporated_water  # Return the result from the original method

        # Replace the original evaporate method with the decorated one
        self.water_tank.evaporate = evaporate_with_concentration_update

    def set_dissolved_elements(self, dissolved_elements: dict):
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

