import asyncio
import json
import os
from threading import Lock
from src.simulation.fish_tank_simulation import FishTankSimulator
from src.simulation.seasonal_weather_simulation import SeasonalWeatherSimulator

class ArtificialEcosystemSimulator:
    def __init__(self, configuration_files_path: str, country: str):
        self.configuration_files_path = None
        self.simulation_config = None
        self._simulation_data = dict()
        self._data_lock = Lock()
        self.configuration_files_lst = self._get_configuration_files(configuration_files_path)
        self._get_simulation_data()
        self.country = country
        self.seasonal_weather_simulator = self._init_seasonal_weather_simulator()
        self.seasonal_weather_simulator.simulation_data = self.simulation_data
        self.fish_tank_simulator = self._init_fish_tank()
        self.fish_tank_simulator.simulation_data = self.simulation_data
        self.sim_tasks = dict()

    @property
    def simulation_data(self):
        with self._data_lock:
            return self._simulation_data

    @simulation_data.setter
    def simulation_data(self, new_data: dict):
        with self._data_lock:
            self._simulation_data = new_data

    
    def _get_configuration_files(self, path: str):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_dir, path)
        self.configuration_files_path = config_path
        # Check if the directory exists
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"The specified configuration files path does not exist: '{config_path}'. "
                "Please ensure the path is correct."
            )

        # Ensure the path is actually a directory
        if not os.path.isdir(config_path):
            raise NotADirectoryError(
                f"The specified path is not a directory: '{config_path}'. Please provide a valid directory path."
            )

        # Get the list of files
        files = os.listdir(config_path)
        if not files:
            raise FileNotFoundError(
                f"The directory {config_path} exists but contains no configuration files. "
                "Please add the required configuration files before proceeding."
            )

        return files

    def _get_simulation_data(self):
        for config_file in self.configuration_files_lst:
            if "simulation" in config_file:
                with open(os.path.join(self.configuration_files_path, config_file), "r") as f:
                    self.simulation_config = json.load(f)

    def _init_seasonal_weather_simulator(self):
        country = self.country.lower()
        for config_file in self.configuration_files_lst:
            if country in config_file and "seasonal_weather" in config_file:
                with open(os.path.join(self.configuration_files_path, config_file), "r") as f:
                    seasonal_weather_config = json.load(f)
                return SeasonalWeatherSimulator(**seasonal_weather_config)

    def _init_fish_tank(self):
        for config_file in self.configuration_files_lst:
            if 'fish_tank' in config_file:
                with open(os.path.join(self.configuration_files_path, config_file), "r") as f:
                    fish_tank_config = json.load(f)
                return FishTankSimulator(**fish_tank_config)

    async def simulate(self):
        seasonal_weather_task = asyncio.create_task(self.seasonal_weather_simulator.simulate(self.simulation_config, True))
        self.sim_tasks['seasonal_weather'] = seasonal_weather_task
        fish_tank_task = asyncio.create_task(self.fish_tank_simulator.simulate(self.simulation_config))
        self.sim_tasks['fish_tank'] = fish_tank_task

        while True:
            try:
                await asyncio.sleep(1)
                if seasonal_weather_task.done():
                    break
            except asyncio.CancelledError:
                # Perform cleanup (if necessary)
                break



if __name__ == '__main__':
    simulator = ArtificialEcosystemSimulator(configuration_files_path="configurations",
                                             country="Austria")
    try:
        asyncio.run(simulator.simulate())
    finally:
        for task in simulator.sim_tasks.values():
            task.cancel()