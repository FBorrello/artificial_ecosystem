### Water Component

**Implementation Requirements:**
- **Water Flow:** The water should flow from higher elevation areas to lower ones with a flow rate that can be adjusted based on terrain slope.
  - **Method:** `flow_water(self, terrain_map)`
    - **Parameters:** 
      - `terrain_map`: A 2D array representing the elevation of each cell in the ecosystem.
    - **Behavior:** Simulates water movement. Water moves from cells with higher elevation to adjacent cells with lower elevation, respecting the terrain's slope. The method should update the water volume in each cell accordingly.

- **Evaporation:** Water should evaporate based on temperature and surface area.
  - **Method:** `evaporate_water(self, temperature, surface_area)`
    - **Parameters:**
      - `temperature`: The current temperature affecting evaporation rate.
      - `surface_area`: The area of water exposed to air.
    - **Behavior:** Calculates and removes a volume of water based on evaporation rate influenced by temperature and surface area.

- **Precipitation:** Simulate rain or snow adding water to the ecosystem.
  - **Method:** `add_precipitation(self, precipitation_type, amount)`
    - **Parameters:**
      - `precipitation_type`: String indicating "rain" or "snow".
      - `amount`: Amount of precipitation (in appropriate units).
    - **Behavior:** Adds water to the system, with snow accumulation if applicable, which melts over time based on temperature.

- **Water Storage:** Some areas can hold more water than others based on soil type or artificial reservoirs.
  - **Method:** `update_storage_capacity(self, soil_type, structures)`
    - **Parameters:**
      - `soil_type`: Affects how much water the ground can hold.
      - `structures`: Presence of reservoirs or other water storage structures.
    - **Behavior:** Updates the capacity of water each cell can hold based on soil and structures.

### Water Component Testing

**Testing Requirements:**
- **Flow Testing:** Ensure water flows correctly down slopes.
  - **Test Case:** `test_water_flow`
    - **Setup:** A grid with a clear slope from one corner to another.
    - **Action:** Call `flow_water` method.
    - **Expected:** Water moves from higher to lower elevation cells.

- **Evaporation Testing:** Check if evaporation reduces water volume appropriately.
  - **Test Case:** `test_evaporation`
    - **Setup:** A cell with known water volume, temperature, and area.
    - **Action:** Call `evaporate_water` method.
    - **Expected:** Water volume decreases according to the evaporation formula.

- **Precipitation Testing:** Verify the addition of water via precipitation.
  - **Test Case:** `test_add_precipitation`
    - **Setup:** Empty cells.
    - **Action:** Call `add_precipitation` with either rain or snow.
    - **Expected:** Correct increase in water volume or snow accumulation.

- **Storage Capacity Testing:** Ensure that storage capacity adjusts with soil and structures.
  - **Test Case:** `test_update_storage_capacity`
    - **Setup:** Different cells with varying soil types and structures.
    - **Action:** Call `update_storage_capacity`.
    - **Expected:** Storage capacity reflects soil type and structure presence.