import tkinter
import matplotlib.pyplot as plt
import asyncio
import json
from src.simulation.water.water_tank import WaterTank
import matplotlib
import random
import traceback
from datetime import datetime, timedelta
from src.simulation.common import get_date_time_simulation_data

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

    def __new__(cls, name, bases, dct):
        dct['fish_tank'] = dict()
        return super().__new__(cls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        # Intercept object instantiation and set seasonal_weather_data
        obj = super().__call__(*args, **kwargs)
        return obj

class FishTankSimulator(metaclass=SimulatorMeta):
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

    def __init__(self, **kwargs):
        """
        Initializes the FishTankSimulator instance.
    
        Initializes key attributes needed for the simulation, including data storage for
        simulation results, history of water tank volumes, simulated duration, and tasks
        for real-time plotting.
        """
        super().__init__()
        kwargs.update({'tank_type': 'fish_tank'})
        self.fish_tank = WaterTank(**kwargs)
        self.simulation_data = dict()
        self.fish_tank_volume_history = []
        self.simulated_seconds = 0
        self.plot_tasks = dict()

    def simulate_evaporation(self, air_temp, surface_area, rel_humidity, time_elapsed_sec):
        """
        Simulates water evaporation from the tank based on weather conditions.
    
        Args:
            air_temp (float): The air temperature during the simulation step.
            surface_area (float): The water surface area exposed to evaporation.
            rel_humidity (float): The relative humidity (0–1) of the air.
            time_elapsed_sec (int): The elapsed simulation time in seconds.
        """
        water_evaporated_amount = self.fish_tank.evaporate(air_temp, surface_area, rel_humidity, time_elapsed_sec)
        if self.simulation_data.get('water_evaporated') is None:
            self.simulation_data['water_evaporated'] = []
        self.simulation_data['water_evaporated'].append(water_evaporated_amount)

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

    def apply_seasonal_weather_data_to_sim(self, sim_date_time, sampling_rate):

        precipitation_volume = self.simulation_data.get('precipitation_volume')
        if precipitation_volume:
            precipitation_volume = precipitation_volume[-1]
            if precipitation_volume > 0:
                self.fish_tank.add_water(precipitation_volume)

        air_temp = self.simulation_data.get('air_temperature')
        if air_temp:
            air_temp = air_temp[-1]
            if air_temp > 0:
                rel_humidity = self.simulation_data.get('relative_humidity')
                if rel_humidity:
                    rel_humidity = rel_humidity[-1]
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

    async def simulate(self, simulation_config: dict, plot: bool = False):
        """
        Runs the fish tank simulation for the configured duration.
    
        Executes the simulation of precipitation, evaporation, and seasonal weather
        effects over time. Updates stored simulation data and manages real-time
        plotting tasks.
    
        Uses asynchronous operations to update plots during each simulation step.
        """
        start_date_time, sim_duration, sampling_rate = get_date_time_simulation_data(simulation_config)
        date_time = start_date_time

        while self.simulated_seconds < sim_duration:
            if plot:
                self.plot_tasks.update(self.detect_sim_data(self.simulation_data))
            try:
                self.apply_seasonal_weather_data_to_sim(date_time, sampling_rate)
            except Exception as e:
                print(f'Error applying seasonal weather data: {e}')
                traceback.print_exc()

            # Update tank water volume data
            if self.simulation_data.get('tank_water_volume') is None:
                self.simulation_data['tank_water_volume'] = []
            self.simulation_data['tank_water_volume'].append(self.fish_tank.current_volume)

            # Simulate async time progression
            await asyncio.sleep(0.001)  # Speed up time.

            self.simulated_seconds += sampling_rate
            date_time += timedelta(seconds=sampling_rate)
