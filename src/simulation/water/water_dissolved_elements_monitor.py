from src.simulation.water.water_property_range import WaterPropertyRange
from src.simulation.water.water_tank import WaterTank

class WaterDissolvedElementsMonitor:
    def __init__(self, water_tank: WaterTank, dissolved_elements: dict):
        if not isinstance(water_tank, WaterTank):
            raise TypeError("The `water_tank` parameter must be a `WaterTank` instance.")
        self.water_tank = water_tank
        self.set_dissolved_elements(dissolved_elements)

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
                    return class_instance.__dict__.get(f"_{e}", 0)

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
                    class_instance.__dict__[f"_{e}"] = value

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
            setattr(self, element, initial_value)
            setattr(self, f"{element}_range", element_range)
