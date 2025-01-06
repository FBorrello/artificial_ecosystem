import asyncio
import json
import os

from src.simulation.seasonal_weather_simulation import SeasonalWeatherSimulator

class ArtificialEcosystemSimulator:
    def __init__(self, configuration_files_path: str, country: str):
        self.configuration_files_path = None
        self.simulation_data = None
        self.configuration_files_lst = self._get_configuration_files(configuration_files_path)
        self._get_simulation_data()
        self.country = country
        self.seasonal_weather_simulator = self._init_seasonal_weather_simulator()
        self.sim_tasks = dict()


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
                    simulation_data = json.load(f)
                self.simulation_data = simulation_data

    def _init_seasonal_weather_simulator(self):
        country = self.country.lower()
        for config_file in self.configuration_files_lst:
            if country in config_file and "seasonal_weather" in config_file:
                with open(os.path.join(self.configuration_files_path, config_file), "r") as f:
                    seasonal_weather_config = json.load(f)
                return SeasonalWeatherSimulator(**seasonal_weather_config)

    async def simulate(self):
        seasonal_weather_task = asyncio.create_task(self.seasonal_weather_simulator.simulate(self.simulation_data))
        self.sim_tasks['seasonal_weather'] = seasonal_weather_task
        weather_sim_data = self.seasonal_weather_simulator.simulation_data

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