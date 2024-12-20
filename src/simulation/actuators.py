import logging
from enum import Enum

# Configure logging
logging.basicConfig(filename='actuators.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ActuatorState(Enum):
    IDLE = "IDLE"
    ON = "ON"
    OFF = "OFF"

class ActuatorError(Exception):
    """Custom exception for actuator errors"""
    pass

class Actuator:
    """
    Base class for actuators in a system.

    Attributes:
        actuator_id (str): Unique identifier for each actuator.
        type (str): Type of actuator (e.g., "fan", "valve", "servo").
        state (ActuatorState): Current state of the actuator.
        location (tuple): Position in the environment or system.

    Methods:
        activate(): Activates the actuator.
        deactivate(): Deactivates the actuator.
        status(): Returns current status of the actuator.
    """

    def __init__(self, actuator_id, type, location):
        if not isinstance(actuator_id, str) or not actuator_id:
            raise ActuatorError("Invalid actuator_id. Must be a non-empty string.")
        self.actuator_id = actuator_id
        self.type = type
        self.state = ActuatorState.IDLE
        self.location = location
        logging.info(f"Actuator {self.actuator_id} initialized at location {self.location}")

    def activate(self):
        """
        Activates or starts the actuator. Logs the state change.
        """
        if self.state != ActuatorState.ON:
            self.state = ActuatorState.ON
            logging.info(f"Actuator {self.actuator_id} activated")

    def deactivate(self):
        """
        Deactivates or stops the actuator. Logs the state change.
        """
        pass