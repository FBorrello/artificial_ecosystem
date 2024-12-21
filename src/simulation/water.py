# src/simulation/water.py

class Water:
    def __init__(self):
        self.water_volume = []
        self.storage_capacity = 0

    def set_water_volume(self, volume):
        """Set the water volume for each cell in the ecosystem."""
        self.water_volume = volume

    def get_water_volume(self):
        """Return the current water volume distribution."""
        return self.water_volume

    def flow_water(self, terrain_map):
        """Simulate water flow based on terrain slope."""
        new_volume = [[0 for _ in row] for row in terrain_map]
        for i in range(len(terrain_map)):
            for j in range(len(terrain_map[0])):
                if self.water_volume[i][j] > 0:
                    # Check adjacent cells for lower elevation
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nx, ny = i + dx, j + dy
                        if 0 <= nx < len(terrain_map) and 0 <= ny < len(terrain_map[0]):
                            if terrain_map[nx][ny] < terrain_map[i][j]:
                                # Determine flow based on elevation difference
                                flow = self.water_volume[i][j] * 0.1  # Example flow fraction
                                new_volume[i][j] -= flow
                                new_volume[nx][ny] += flow
        self.water_volume = new_volume

    def evaporate_water(self, temperature, surface_area):
        """Simulate evaporation of water based on temperature and surface area."""
        evaporation_rate = temperature * surface_area * 0.001  # Simplified evaporation rate calculation
        for i, row in enumerate(self.water_volume):
            for j, volume in enumerate(row):
                if volume > evaporation_rate:
                    self.water_volume[i][j] -= evaporation_rate

    def add_precipitation(self, precipitation_type, amount):
        """Add precipitation to the ecosystem."""
        for i, row in enumerate(self.water_volume):
            for j, _ in enumerate(row):
                if precipitation_type == "rain":
                    self.water_volume[i][j] += amount
                elif precipitation_type == "snow":
                    # Snow accumulation, might need further logic for melting
                    self.water_volume[i][j] += amount / 10  # Assume snow compacts to 1/10th volume

    def update_storage_capacity(self, soil_type, structures=False):
        """Update the water storage capacity based on soil type and structures."""
        if soil_type == 'clay':
            self.storage_capacity = 50  # Example capacity for clay
        elif soil_type == 'sand':
            self.storage_capacity = 200  # Example capacity for sand
        if structures:
            self.storage_capacity += 100  # Increase capacity if structures present

    def get_storage_capacity(self):
        """Return the current storage capacity."""
        return self.storage_capacity