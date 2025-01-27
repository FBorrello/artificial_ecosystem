import math
import tkinter
import matplotlib.pyplot as plt
import asyncio
import matplotlib
import random
from datetime import datetime, timedelta
from src.simulation.common import get_date_time_simulation_data

matplotlib.use('TkAgg')  # Explicitly use the Tkinter-based backend
plt.style.use('dark_background')  # Use the dark background style


class SeasonalWeatherSimulatorMeta(type):
    def __new__(cls, name, bases, dct):
        dct['seasonal_weather_data'] = dict()
        return super().__new__(cls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        # Intercept object instantiation and set seasonal_weather_data
        obj = super().__call__(*args, **kwargs)
        weather_data = kwargs
        cls._validate_weather_data(weather_data)
        obj.__class__.seasonal_weather_data = weather_data
        return obj

    @staticmethod
    def _validate_weather_data(seasonal_weather_data):
        if not isinstance(seasonal_weather_data, dict):
            raise ValueError("Invalid seasonal weather data. Expected dictionary.")
        elif not seasonal_weather_data:
            raise ValueError("Seasonal weather data is empty.")
        required_keys = ['rain', 'snow', 'temperature', 'relative_humidity']
        for month, data in seasonal_weather_data.items():
            for key in required_keys:
                if key not in data:
                    raise ValueError(f"Missing key '{key}' in weather data for {month}")


class SeasonalWeatherSimulator(metaclass=SeasonalWeatherSimulatorMeta):
    def __init__(self, **kwargs):
        super().__init__()
        self.simulation_data = dict()
        self.simulated_seconds = 0
        self.plot_tasks = dict()
        self.roof_surface = 0
        self.plot_grid = {
            "rain_section": {
                "row_1": [],
                "row_2": [],
                "row_3": [],
                "row_4": []},
            "snow_section": {
                "row_1": [],
                "row_2": [],
                "row_3": [],
                "row_4": []}
            }

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
            ((total_precipitation_days * 24 * 60 * 60) - len(
                self.simulation_data.get(precipitation_type).get(month) * sampling_rate), 0))

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
            (total_precipitation_amount_liters - sum(self.simulation_data.get(precipitation_type).get(month)), 0))

        # If there is remaining precipitation, simulate distribution over seconds
        if round(remaining_precipitation_amount_liters) > 0 and round(total_precipitation_seconds_remaining) > 0:
            # Use randomized weighting to simulate varying precipitation over the remaining time
            random_weight = random.uniform(0.5, 1.5)  # Random weight introduces variability
            remaining_precipitation_amount_liters_second = (
                    (remaining_precipitation_amount_liters / total_precipitation_seconds_remaining) *
                    random_weight * sampling_rate
            )

            # Further randomize precipitation patterns (steady or intermittent)
            precipitation_patterns = ['steady', 'intermittent'][random.randrange(0, 2)]

            # Optionally, add phasic or cyclic variation (simulate peaks and troughs like real weather events)
            cyclic_variation = max(0.5, math.sin(
                2 * math.pi * (1 - total_precipitation_seconds_remaining / (
                            30 * 24 * 60 * 60))) + 1)  # Sinusoidal variation
            precipitation_amount = (
                    random.uniform(0.7, 1.3) *
                    remaining_precipitation_amount_liters_second *
                    cyclic_variation
            )

            return precipitation_amount
        return 0

    async def plot_sim_data(self,
                            plot_name: str,
                            y_label: str,
                            data_reference: list,
                            main_plot: bool = False,
                            monitor_width=3840,
                            monitor_height=1920):
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

    def detect_sim_data(self, sim_data, name: str = None):
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
        rain_amount = 0
        snow_amount = 0
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

            if not self.simulation_data.get('air_temperature'):
                self.simulation_data['air_temperature'] = []
            self.simulation_data['air_temperature'].append(air_temp)

            if not self.simulation_data.get('relative_humidity'):
                self.simulation_data['relative_humidity'] = []
            self.simulation_data['relative_humidity'].append(month_season_data.get('relative_humidity')[hour] / 100)

        return rain_amount + snow_amount

    async def simulate(self, simulation_config: dict, plot: bool = False):

        start_date_time, sim_duration, sampling_rate = get_date_time_simulation_data(simulation_config)
        date_time = start_date_time
        self.roof_surface = simulation_config.get('roof_surface')

        while self.simulated_seconds < sim_duration:
            if plot:
                self.plot_tasks.update(self.detect_sim_data(self.simulation_data))

            # Update precipitation_volume data
            if self.simulation_data.get('precipitation_volume') is None:
                self.simulation_data['precipitation_volume'] = []
            precipitation_amount = self.apply_seasonal_weather_data_to_sim(date_time, sampling_rate)
            self.simulation_data['precipitation_volume'].append(precipitation_amount)

            # Simulate async time progression
            await asyncio.sleep(0.001)  # Speed up time.

            self.simulated_seconds += sampling_rate
            date_time += timedelta(seconds=sampling_rate)

        # Prevent process termination
        input("Simulation completed. Press Enter to exit and close windows.")
