# src/simulation/models.py


class Fish:
    """
    Represents a fish in the artificial ecosystem. This class models the fish's attributes
    and behaviors within the ecosystem simulation.

    Attributes:
        species (str): The species of the fish.
        size (float): The size of the fish, which can affect its role in the ecosystem.
        health (float): The health status of the fish, impacting its survival.
        age (int): The age of the fish, influencing its growth and reproductive capabilities.
        is_predatory (bool): Flag indicating if the fish is predatory.
        position (list): The current position of the fish in the ecosystem.
        energy (int): The energy level of the fish, affecting its ability to move and survive.
    """

    def __init__(self, species, size, health, age, is_predatory=False):
        """Initialize a new Fish instance with given attributes."""
        self.species = species
        self.size = size
        self.health = health
        self.age = age
        self.is_predatory = is_predatory
        self.position = [0, 0]  # Initial position in a 2D space
        self.energy = 100  # Starting energy level

    def move(self, dx, dy):
        """
        Move the fish by dx units horizontally and dy units vertically.

        Args:
            dx (float): Horizontal movement.
            dy (float): Vertical movement.
        """
        self.position[0] += dx
        self.position[1] += dy
        self.energy -= 1  # Movement consumes energy

    def eat(self, food):
        """
        The fish consumes food, increasing its health and energy.

        Args:
            food (object): An object representing food with nutritional value and energy boost.
        """
        self.health += food.nutritional_value
        self.energy += food.energy_boost

    def grow(self):
        """Simulate growth of the fish, increasing size and health."""
        self.size += 0.1  # Growth rate
        self.health += 0.5  # Health improvement with growth

    def age_up(self):
        """Increment the age of the fish and decrease its health slightly with aging."""
        self.age += 1
        self.health -= 0.2  # Ageing impacts health

    def reproduce(self):
        """
        Simulate reproduction. Returns a new Fish instance similar to the parent.

        Returns:
            Fish: A new fish of the same species, half the size, full health, and zero age.
        """
        if self.is_predatory:
            return Fish(self.species, self.size * 0.5, 100, 0, True)
        else:
            return Fish(self.species, self.size * 0.5, 100, 0)

    def is_alive(self):
        """
        Check if the fish is still alive based on its health and energy.

        Returns:
            bool: True if the fish is alive, False otherwise.
        """
        return self.health > 0 and self.energy > 0

    def __str__(self):
        """Return a string representation of the Fish instance."""
        return f"{self.species} fish of size {self.size}, age {self.age}, health {self.health}, energy {self.energy}"


class Plant:
    """
    Represents a plant in the artificial ecosystem. Plants are crucial for the ecosystem,
    providing oxygen, habitat, and food.

    Attributes:
        species (str): The species of the plant.
        growth_rate (float): Rate at which the plant grows. Can affect the oxygen production.
        health (float): The health status of the plant, impacting its survival.
        nutrient_requirement (dict): Dictionary specifying the nutrients needed for growth.
        position (list): The current position of the plant in the ecosystem.

    Methods:
        grow(): Simulates growth of the plant, increasing its size and health.
        absorb_nutrients(nutrients): Absorbs nutrients from the environment, affecting health.
        produce_oxygen(): Simulates the plant's role in oxygen production.
    """

    def __init__(self, species, growth_rate, health, nutrient_requirement):
        """Initialize a new Plant instance with given attributes."""
        self.species = species
        self.growth_rate = growth_rate
        self.health = health
        self.nutrient_requirement = nutrient_requirement
        self.position = [0, 0]  # Assuming 2D space for simplicity

    def grow(self):
        """Simulate growth of the plant, increasing health based on growth rate."""
        self.health += self.growth_rate

    def absorb_nutrients(self, nutrients):
        """
        Absorb nutrients from the environment, increasing health if requirements met.

        Args:
            nutrients (dict): Available nutrients in the environment.
        """
        absorbed = 0
        for nutrient, amount in self.nutrient_requirement.items():
            if nutrient in nutrients and nutrients[nutrient] >= amount:
                absorbed += amount
                nutrients[nutrient] -= amount
        self.health += absorbed  # Health increases with nutrient absorption

    def produce_oxygen(self):
        """Simulate oxygen production based on the plant's health."""
        return self.health * 0.01  # Simplified model where oxygen production is proportional to health

    def __str__(self):
        """Return a string representation of the Plant instance."""
        return f"{self.species} plant with health {self.health}, growth rate {self.growth_rate}"


class Environment:
    """
    Represents the environment of the artificial ecosystem. This class manages
    the physical and chemical conditions of the ecosystem.

    Attributes:
        temperature (float): Current temperature of the environment.
        light_level (float): Current light intensity affecting photosynthesis.
        nutrients (dict): Dictionary of available nutrients like nitrogen, phosphorus.
        ph_level (float): pH level of the water, affecting plant and fish health.
    """

    def __init__(self, temperature, light_level, nutrients, ph_level):
        """Initialize the environment with given parameters."""
        self.temperature = temperature
        self.light_level = light_level
        self.nutrients = nutrients
        self.ph_level = ph_level

    def adjust_temperature(self, delta):
        """
        Adjust the environment's temperature by the given delta.

        Args:
            delta (float): Change in temperature, can be positive or negative.
        """
        self.temperature += delta

    def adjust_light(self, delta):
        """
        Adjust the light level in the environment.

        Args:
            delta (float): Change in light level, can be positive or negative.
        """
        self.light_level = max(0, self.light_level + delta)

    def replenish_nutrients(self, nutrient_dict):
        """
        Add nutrients to the environment.

        Args:
            nutrient_dict (dict): Dictionary of nutrients and their quantities to add.
        """
        for nutrient, amount in nutrient_dict.items():
            if nutrient in self.nutrients:
                self.nutrients[nutrient] += amount
            else:
                self.nutrients[nutrient] = amount

    def __str__(self):
        """Return a string representation of the Environment instance."""
        return f"Environment: Temp {self.temperature}, Light {self.light_level}, Nutrients {self.nutrients}, pH {self.ph_level}"
