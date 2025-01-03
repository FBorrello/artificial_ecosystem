import tkinter
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
        dct['fish_tank'] = WaterTank(**sim_config['fish_tank'])
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
        fish_tank_volume_history (list): History of water volumes in the tank.
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
        self.fish_tank_volume_history = []
        self.simulated_seconds = 0
        self.plot_tasks = dict()
        self._validate_weather_data()

    def _validate_weather_data(self):
        """
        Validates the seasonal weather data in the configuration.
    
        Checks that the required keys ('rain', 'snow', 'temperature', and 'humidity')
        are present for each month's weather data. If any key is missing, a 
        ValueError is raised indicating the missing key and the corresponding month.
    
        Raises:
            ValueError: If any of the required keys are missing in weather data for a particular month.
        """
        required_keys = ['rain', 'snow', 'temperature', 'humidity']
        for month, data in self.seasonal_weather_data.items():
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing key '{key}' in weather data for {month}")

    @staticmethod
    def calculate_snow_density(temp: float) -> float:
        """
        Calculates the density of snow based on the given air temperature.
        
        Args:
            temp (float): The air temperature in degrees Celsius.
        
        Returns:
            float: The density of snow (in g/cm³) based on temperature. 
                - Powder snow: 0.1 for temperatures below -5°C.
                - Wet snow: 0.3 for temperatures between -5°C and 0°C.
                - Slush: 0.5 for temperatures above 0°C (near melting point).
        """
        if not isinstance(temp, float):
            raise ValueError("Invalid temperature value. Expected float.")

        if temp < -5:
            return 0.1  # Powder snow
        elif -5 <= temp <= 0:
            return 0.3  # Wet snow
        else:
            return 0.5  # Slush (near melting point)

    def simulate_precipitation(self,
                               precipitation_type: str,
                               month: str,
                               month_season_data: dict,
                               air_temp: float,
                               sampling_rate: int) -> float:
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
        # Calculate the total remaining precipitation seconds based on average days
        total_precipitation_days = precipitation_season_data.get('average_days')
        total_precipitation_seconds_remaining = max(
            (total_precipitation_days * 24 * 60 * 60) - len(
                self.simulation_data.get(precipitation_type).get(month) * sampling_rate), 0)

        # Calculate the total precipitation amount in liters
        total_precipitation_amount_mm = precipitation_season_data.get('total_mm')
        total_precipitation_amount_liters = 0
        if precipitation_type == 'rain':
            # Rain: Use roof surface to calculate water volume
            total_precipitation_amount_liters = total_precipitation_amount_mm * self.roof_surface
        elif precipitation_type == 'snow':
            # Snow: Apply density factor to calculate equivalent water volume
            snow_density_factor = self.calculate_snow_density(air_temp)
            total_precipitation_amount_liters = total_precipitation_amount_mm * self.roof_surface * snow_density_factor

        # Calculate remaining precipitation amount
        remaining_precipitation_amount_liters = max(
            total_precipitation_amount_liters - sum(self.simulation_data.get(precipitation_type).get(month)), 0)

        # If there is remaining precipitation, simulate distribution over seconds
        if round(remaining_precipitation_amount_liters) > 0 and round(total_precipitation_seconds_remaining) > 0:
            remaining_precipitation_amount_liters_second = (remaining_precipitation_amount_liters /
                                                            total_precipitation_seconds_remaining * sampling_rate)
            # Randomize precipitation patterns (steady or intermittent)
            precipitation_patterns = ['steady', 'intermittent'][random.randrange(0, 2)]
            # Add randomized precipitation amount
            precipitation_amount = random.randrange(
                0, int(remaining_precipitation_amount_liters_second * 1000000) *
                   random.randrange(1, 10)) / 1000000

            self.fish_tank.manage_precipitation(precipitation_type,
                                                 precipitation_amount,
                                                 air_temp,
                                                 precipitation_patterns)
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
        self.fish_tank.evaporate(air_temp, surface_area, rel_humidity, time_elapsed_sec)

    async def plot_sim_data(self,
                            plot_name: str,
                            y_label: str,
                            data_reference: list,
                            main_plot: bool = False,
                            monitor_width=3840,
                            monitor_height=1920):
        """
        Asynchronously generates a real-time line plot for simulation data.
    
        This method creates a non-blocking interactive plot that updates dynamically 
        as new data points are added to the provided data reference. It is designed 
        to run as an asynchronous task, allowing other simulation processes to 
        continue while plotting.
    
        Args:
            plot_name (str): The title of the plot.
            y_label (str): The label for the plot's vertical axis.
            data_reference (list): A list that stores the data points to be plotted over time.
            main_plot (bool, optional): Indicates whether this is the main plot. Defaults to False.
            monitor_width (int, optional): Width of the monitor in pixels. Defaults to 3840.
            monitor_height (int, optional): Height of the monitor in pixels. Defaults to 1920.
    
        Behavior:
            - Continuously monitors `data_reference` for new data points.
            - Updates the plot in real time as data points are appended to `data_reference`.
            - Runs indefinitely until the simulation ends or the task is canceled.
        """
        plt.ion()  # Enable interactive mode to allow non-blocking updates
        dpi = 100  # Assuming 100 DPI (dots per inch)
        width = monitor_width / 6
        height = ((monitor_height / 3) * 2) / 4
        if main_plot:
            width = monitor_width
            height = monitor_height / 3
        # Create a new figure and axis for the plot with custom size
        fig, ax = plt.subplots(figsize=(width / dpi, height / dpi))
        ax.set_title(plot_name)  # Set the plot title
        ax.set_xlabel("Time Steps")  # Label for the horizontal axis
        ax.set_ylabel(f'{y_label} liters')  # Label for the vertical axis
        fig.canvas.manager.set_window_title(plot_name)  # Set window title

        plt.pause(1)
        x, y = 0, 0
        if not main_plot:
            y = monitor_height / 3 + 35
            if 'rain' in plot_name:
                row_counter = 0
                for row, columns_lst in self.plot_grid.get('rain_section').items():
                    if len(columns_lst) < 3:
                        y += row_counter * height + 30 * row_counter
                        x = len(columns_lst) * width
                        columns_lst.append((x, y))
                        break
                    else:
                        row_counter += 1
            elif 'snow' in plot_name:
                row_counter = 0
                for row, columns_lst in self.plot_grid.get('snow_section').items():
                    if len(columns_lst) < 3:
                        y += row_counter * height + 30 * row_counter
                        x = len(columns_lst) * width + (monitor_width / 2)
                        columns_lst.append((x, y))
                        break
                    else:
                        row_counter += 1

        def move_window(event):
            manager = event.canvas.manager
            if hasattr(manager, 'window') and isinstance(manager.window, tkinter.Tk):
                manager.window.wm_geometry(f"+{int(x)}+{int(y)}")
                # Remove plot elements (toolbar, axis, etc.)
                manager.toolbar.pack_forget()  # Hides the toolbar

        # Inside the `plot_sim_data` method, after creating `fig`:
        fig.canvas.mpl_connect("draw_event", move_window)

        plt.show(block=False)  # Show the plot window without blocking execution
        prev_len = 0  # Track the length of data_reference to detect new data points

        while True:
            if len(data_reference) > prev_len:  # Check if new data has been added
                ax.clear()  # Clear the previous plot
                ax.plot(range(1, len(data_reference) + 1),
                        data_reference,
                        label=y_label)  # Plot new data
                ax.legend()  # Add legend to the plot

                plt.pause(0.001)  # Pause briefly to render the plot
                fig.canvas.draw_idle()  # Mark the figure as needing a refresh
                fig.canvas.flush_events()  # Flush GUI events to update the canvas

                prev_len = len(data_reference)  # Update the tracked data length

            await asyncio.sleep(1)  # Wait for 1 second before checking for new data again

    @staticmethod
    def validate_time_units(unit, valid_units):
        if unit not in valid_units:
            raise ValueError(f"Invalid time unit '{unit}'. Supported units are: {', '.join(valid_units)}")

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
        self.validate_time_units(time_unit, unit_to_seconds.keys())
        # Convert the simulation duration into seconds.
        sim_duration = unit_to_seconds.get(time_unit.lower(), 1) * duration

        # Extract the sample unit and convert it to seconds, defaulting to 1 second if unknown.
        sample_unit = self.sample_unit
        self.validate_time_units(sample_unit, unit_to_seconds.keys())
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

        randomize_precipitation = random.randrange(0, 10)
        if 0 <= randomize_precipitation <= 3:
            if air_temp > 3:
                rain_amount = self.simulate_precipitation('rain',
                                                          month,
                                                          month_season_data,
                                                          air_temp,
                                                          sampling_rate)
                self.simulation_data['rain'][month].append(rain_amount)
            else:
                snow_amount = self.simulate_precipitation('snow',
                                                          month,
                                                          month_season_data,
                                                          air_temp,
                                                          sampling_rate)
                self.simulation_data['snow'][month].append(snow_amount)

        if air_temp > 0:
            rel_humidity = month_season_data.get('humidity')[hour] / 100
            self.simulate_evaporation(air_temp, self.fish_tank.water_surface_area, rel_humidity, sampling_rate)

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
                                           data_reference=sim_data,
                                           main_plot=True if name is None else False)
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

        while self.simulated_seconds < sim_duration:
            self.plot_tasks.update(self.detect_sim_data(self.simulation_data))
            self.apply_seasonal_weather_data_to_sim(date_time, sampling_rate)

            # Update tank water volume data
            if self.simulation_data.get('tank_water_volume') is None:
                self.simulation_data['tank_water_volume'] = []
            self.simulation_data['tank_water_volume'].append(self.fish_tank.current_volume)

            # Simulate async time progression
            await asyncio.sleep(0.001)  # Speed up time.

            self.simulated_seconds += sampling_rate
            date_time += timedelta(seconds=sampling_rate)

        # Prevent process termination
        input("Simulation completed. Press Enter to exit and close windows.")


if __name__ == "__main__":
    sim = FishTankSimulator()
    try:
        asyncio.run(sim.simulate())
    finally:
        for name, plot_task in sim.plot_tasks.items():
            plot_task.cancel()  # Stop plotting when the simulation ends.
