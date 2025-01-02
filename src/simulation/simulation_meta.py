from typing import Any

import matplotlib.pyplot as plt
import asyncio
import json
from src.simulation.water.water_tank import WaterTank
import matplotlib
import random
from datetime import datetime, timedelta

matplotlib.use('TkAgg')  # Explicitly use the Tkinter-based backend
plt.style.use('dark_background')  # Use the dark background style

# Load config
with open("./configurations/fish_tank_life_cycle.json", "r") as f:
    config = json.load(f)

class SimulatorMeta(type):
    """
    A metaclass to initialize simulation-related attributes and configuration.
    
    The `SimulatorMeta` class dynamically adds attributes and initializes
    the `WaterTank` instance based on provided simulation configuration
    parameters. It is used to streamline the setup of simulation objects.
    """
    
    def __new__(cls, name, bases, dct, **sim_config):
        dct['water_tank'] = WaterTank(**sim_config['water_tank'])
        # Add attributes from the config to the class
        for key, value in sim_config.get('simulation_config').items():
            dct[key] = value
        return super().__new__(cls, name, bases, dct)

class FishTankSimulator(metaclass=SimulatorMeta, **config):
    """
    A simulator for modeling the dynamics of a fish tank, integrating precipitation,
    evaporation, and seasonal weather effects.

    This class uses configuration parameters to simulate water level management
    within a fish tank, leveraging seasonal weather data and predefined tank
    properties. It supports real-time plotting of simulation results and is capable
    of handling asynchronous tasks such as data visualization.

    Attributes:
        simulation_data (dict): A storage dictionary for simulation results.
        water_tank_volume_history (list): History of water volumes in the tank.
        simulated_seconds (int): Total simulated time in seconds.
        plot_tasks (dict): Tracks asynchronous plotting tasks.
    """
    
    def __init__(self):
        """
        Initializes the FishTankSimulator instance.
    
        Initializes key attributes needed for the simulation, including data storage for
        simulation results, history of water tank volumes, simulated duration, and tasks
        for real-time plotting.
        """
        self.simulation_data = dict()
        self.water_tank_volume_history = []
        self.simulated_seconds = 1
        self.plot_tasks = dict()

    def simulate_precipitation(self, precipitation_type, month, month_season_data, air_temp, sampling_rate):
        """
        Simulates precipitation and its impact on the water tank.
    
        Args:
            precipitation_type (str): The type of precipitation (e.g., 'rain' or 'snow').
            month (str): The current month being simulated.
            month_season_data (dict): Seasonal weather data for the current month.
            air_temp (float): The current air temperature during the simulation.
            sampling_rate (int): The time step in seconds for data sampling.
    
        Returns:
            float: The amount of precipitation added to the water tank.
        """
        precipitation_season_data = month_season_data.get(precipitation_type)
        total_precipitation_days = precipitation_season_data.get('average_days')
        total_precipitation_seconds_remaining = max((total_precipitation_days * 24 * 60 * 60) - len(self.simulation_data.get(precipitation_type).get(month) * sampling_rate), 0)

        total_precipitation_amount_mm = precipitation_season_data.get('total_mm')
        total_precipitation_amount_liters = 0
        if precipitation_type == 'rain':
            total_precipitation_amount_liters = total_precipitation_amount_mm * self.roof_surface
        elif precipitation_type == 'snow':
            snow_density_factor = 0.1  # Density of snow as a factor of water (10%)
            total_precipitation_amount_liters = total_precipitation_amount_mm * self.roof_surface * snow_density_factor / 1000
        remaining_precipitation_amount_liters = max(total_precipitation_amount_liters - sum(self.simulation_data.get(precipitation_type).get(month)), 0)

        if round(remaining_precipitation_amount_liters) > 0 and round(total_precipitation_seconds_remaining) > 0:
            remaining_precipitation_amount_liters_second = remaining_precipitation_amount_liters / total_precipitation_seconds_remaining * sampling_rate
            precipitation_patterns = ['steady', 'intermittent'][random.randrange(0, 2)]
            precipitation_amount = random.randrange(0, int(remaining_precipitation_amount_liters_second * 1000000) * random.randrange(1, 10)) / 1000000
            self.water_tank.manage_precipitation(precipitation_type, precipitation_amount, air_temp, precipitation_patterns)
            return precipitation_amount
        return 0

    def simulate_evaporation(self, air_temp, surface_area, rel_humidity, time_elapsed_sec):
        """
        Simulates water evaporation from the tank based on weather conditions.
    
        Args:
            air_temp (float): The air temperature during the simulation step.
            surface_area (float): The water surface area exposed to evaporation.
            rel_humidity (float): The relative humidity (0–1) of the air.
            time_elapsed_sec (int): The elapsed simulation time in seconds.
        """
        self.water_tank.evaporate(air_temp, surface_area, rel_humidity, time_elapsed_sec)
    
    @staticmethod
    async def plot_sim_data(plot_name: str, y_label: str, data_reference):
        """Asynchronous method to plot water volume."""
        plt.ion()  # Enable interactive mode
        fig, ax = plt.subplots()
        ax.set_title(plot_name)
        ax.set_xlabel("Time Steps")
        ax.set_ylabel(f'{y_label} liters')

        plt.show(block=False)  # Non-blocking show
        prev_len = 0
        while True:
            if len(data_reference) > prev_len:
                ax.clear()
                ax.plot(range(1, len(data_reference) + 1),
                        data_reference,
                        label=y_label)
                ax.legend()

                plt.pause(0.001)
                fig.canvas.draw_idle()  # Mark the figure as "stale," indicating it needs a refresh
                fig.canvas.flush_events()  # Force update of the graphic canvas

                prev_len = len(data_reference)  # Update tracked length

            await asyncio.sleep(1)  # Plot updates every second
    
    def get_date_time_simulation_data(self) -> tuple[datetime, int, int]:
        """
        Extracts and calculates essential time-based simulation parameters.
    
        Returns:
            tuple: A tuple containing:
                - datetime: The start date and time of the simulation.
                - int: The total duration of the simulation in seconds.
                - int: The sampling rate for data collection in seconds.
        """
        # Extract the start date/time and formatting string from the configuration.
        start_date_time = datetime.strptime(self.start_date_time, self.start_date_time_format)
        
        # Define conversion factors for various time units to seconds.
        unit_to_seconds = {
            "second": 1,
            "minute": 60,
            "hour": 3600,
            "day": 86400,
            "week": 604800,
            "month": 30 * 86400,  # Approximation for a month
            "year": 365 * 86400,  # Approximation for a year
        }
        
        # Extract the simulation duration and its unit from the configuration.
        duration = self.duration
        time_unit = self.time_unit
        # Convert the simulation duration into seconds.
        sim_duration = unit_to_seconds.get(time_unit.lower(), 1) * duration
        
        # Extract the sample unit and convert it to seconds, defaulting to 1 second if unknown.
        sample_unit = self.sample_unit
        sampling_rate = unit_to_seconds.get(sample_unit.lower(), 1)  # Default to 1 second if unit is unknown

        # Return the formatted start date/time, total simulation duration, and sampling rate.
        return start_date_time, sim_duration, sampling_rate

    def apply_seasonal_weather_data_to_sim(self, sim_date_time, sampling_rate):
        """
        Applies seasonal weather data to the simulation for a specific time step.
    
        This method updates the simulation data with precipitation (rain or snow)
        and evaporation values based on the current weather conditions and time.
    
        Args:
            sim_date_time (datetime): The current simulated date and time.
            sampling_rate (int): The time step in seconds for data sampling.
        """
        month_mapping = {
            1: "January",
            2: "February",
            3: "March",
            4: "April",
            5: "May",
            6: "June",
            7: "July",
            8: "August",
            9: "September",
            10: "October",
            11: "November",
            12: "December"
        }
        month = month_mapping[sim_date_time.month]
        hour = sim_date_time.hour
        month_season_data = self.seasonal_weather_data.get(month)
        air_temp = month_season_data.get('temperature')[hour] + random.uniform(-1, 1)
        
        
        if self.simulation_data.get('rain') is None:
            self.simulation_data['rain'] = {}
        if self.simulation_data.get('rain').get(month) is None:
            self.simulation_data['rain'][month] = []
        if self.simulation_data.get('snow') is None:
            self.simulation_data['snow'] = {}
        if self.simulation_data.get('snow').get(month) is None:
            self.simulation_data['snow'][month] = []

        if air_temp > 3:
            rain_amount = self.simulate_precipitation('rain', month, month_season_data, air_temp, sampling_rate)
            self.simulation_data['rain'][month].append(rain_amount)
        else:
            snow_amount = self.simulate_precipitation('snow', month, month_season_data, air_temp, sampling_rate)
            self.simulation_data['snow'][month].append(snow_amount)

        if air_temp > 0:
            rel_humidity = month_season_data.get('humidity')[hour] / 100
            self.simulate_evaporation(air_temp, self.water_tank.water_surface_area, rel_humidity, sampling_rate)

    def detect_sim_data(self, sim_data, name: str = None):
        """
        Identifies and asynchronously plots simulation data.
    
        Args:
            sim_data (dict): The nested dictionary structure containing simulation results.
            name (str, optional): A prefix for plot names based on data type or category.
    
        Returns:
            dict: A dictionary of asynchronous tasks for each detected plot.
        """
        plot_tasks = dict()
        for key, sim_data in sim_data.items():
            if isinstance(sim_data, dict):
                plot_tasks.update(self.detect_sim_data(sim_data, name=key))
            elif isinstance(sim_data, list):
                plot_name = f'Plot {name if name is not None else ""} {key}'
                if plot_name not in self.plot_tasks:
                    # Start the plotting coroutine
                    plot_tasks[plot_name] = asyncio.create_task(
                        self.plot_sim_data(plot_name=plot_name,
                                           y_label=f'{name if name is not None else ""} {key}',
                                           data_reference=sim_data)
                    )
        return plot_tasks

    async def simulate(self):
        """
        Runs the fish tank simulation for the configured duration.
    
        Executes the simulation of precipitation, evaporation, and seasonal weather
        effects over time. Updates stored simulation data and manages real-time
        plotting tasks.
    
        Uses asynchronous operations to update plots during each simulation step.
        """
        print(f"Starting simulation: {self.name}")

        start_date_time, sim_duration, sampling_rate = self.get_date_time_simulation_data()
        date_time = start_date_time

        try:
            while self.simulated_seconds < sim_duration:
                self.plot_tasks.update(self.detect_sim_data(self.simulation_data))
                try:
                    self.apply_seasonal_weather_data_to_sim(date_time, sampling_rate)
                except ValueError:
                    self.water_tank.current_volume -= self.water_tank.overflow_capacity_threshold

                # Update tank water volume data
                if self.simulation_data.get('tank_water_volume') is None:
                    self.simulation_data['tank_water_volume'] = []
                self.simulation_data['tank_water_volume'].append(self.water_tank.current_volume)

                # Simulate async time progression
                await asyncio.sleep(0.001)  # Speed up time.

                self.simulated_seconds += sampling_rate
                date_time += timedelta(seconds=sampling_rate)
                

            # Print completion message
            print("Simulation complete!")
        finally:
            for name, plot_task in self.plot_tasks.items():
                plot_task.cancel()  # Stop plotting when the simulation ends.

if __name__ == "__main__":
    sim = FishTankSimulator()
    asyncio.run(sim.simulate())