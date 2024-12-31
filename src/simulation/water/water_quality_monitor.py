from src.simulation.water.water_property_range import WaterPropertyRange

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
