import numpy as np
import matplotlib.pyplot as plt


class FishTankSimulation:
    def __init__(self, volume_liters, initial_fish_count, initial_temperature, initial_ph, initial_ammonia):
        self.volume = volume_liters
        self.fish = [Fish() for _ in range(initial_fish_count)]
        self.temperature = initial_temperature
        self.ph = initial_ph
        self.ammonia = initial_ammonia
        self.nitrite = 0.0
        self.nitrate = 0.0
        self.oxygen = 8.0  # mg/L, typical saturation level
        self.time = 0
        self.time_step = 0.1  # days, assuming daily updates

    def update_environment(self):
        # Temperature might change due to external conditions or equipment
        self.temperature += np.random.normal(0, 0.1)  # Small daily fluctuation

        # Ammonia increases with fish waste, decreases with filtration
        self.ammonia += (len(self.fish) * 0.01) - (0.05 * self.ammonia)  # Arbitrary rate

        # Simplified nitrogen cycle
        self.nitrite += (0.2 * self.ammonia) - (0.1 * self.nitrite)
        self.nitrate += (0.1 * self.nitrite) - (0.01 * self.nitrate)  # Water changes would reduce this

        # pH can drift slightly each day
        self.ph += np.random.normal(0, 0.01)

        # Oxygen consumption by fish, replenished by plants or aeration
        self.oxygen -= (len(self.fish) * 0.05) + np.random.normal(0, 0.1)
        self.oxygen = max(0, min(10, self.oxygen))  # Clamp between 0 and 10 mg/L

    def update_fish_population(self):
        # Fish health and population changes based on environment
        for fish in self.fish[:]:  # Iterate over a copy to safely modify the list
            if fish.check_health(self.temperature, self.ph, self.oxygen, self.ammonia) == "dead":
                self.fish.remove(fish)
            elif np.random.random() < 0.01:  # Small chance to breed if conditions are good
                self.fish.append(Fish())

    def run_simulation(self, days):
        temp_history = []
        fish_count_history = []
        for day in range(int(days / self.time_step)):
            self.update_environment()
            self.update_fish_population()
            self.time += self.time_step
            temp_history.append(self.temperature)
            fish_count_history.append(len(self.fish))

        # Simple visualization
        plt.figure(figsize=(10, 5))
        plt.plot(np.arange(0, days, self.time_step), temp_history, label="Temperature")
        plt.plot(np.arange(0, days, self.time_step), fish_count_history, label="Fish Count")
        plt.xlabel('Days')
        plt.ylabel('Value')
        plt.legend()
        plt.title('Fish Tank Simulation')
        plt.show()


class Fish:
    def check_health(self, temp, ph, oxygen, ammonia):
        if temp < 20 or temp > 30 or ph < 6.5 or ph > 8.0 or oxygen < 5 or ammonia > 0.25:
            return "dead"
        return "alive"


# Example usage
tank = FishTankSimulation(volume_liters=100, initial_fish_count=5, initial_temperature=25, initial_ph=7.0,
                          initial_ammonia=0.0)
tank.run_simulation(days=365)