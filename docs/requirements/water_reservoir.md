# In-Depth Report: Water Reservoir for Artificial Ecosystem Prototype

This report details the design, thermal properties, and cost of the water reservoir, a critical component of the artificial ecosystem prototype. It serves as a fish tank and a major thermal mass contributor, enabling year-round temperature stability at 20°C.

---

## **Design Specifications**
- **Location**: Buried underground.
- **Structure**: Self-contained in a sinking concrete cylindrical structure.
- **Outer Layer**: 20 cm annular gap filled with clay pebbles for thermal mass.
- **Dimensions**: 5-meter diameter, 3-meter depth.

---

## **Design and Implementation**
### **Structure**
- **Inner Cylinder**: Reinforced concrete, 5 m diameter, 3 m deep, waterproofed to hold water and fish (tilapia).
- **Outer Shell**: Concrete cylinder, 5.4 m diameter, creating a 20 cm gap around the inner tank.
- **Clay Pebbles**: Fill the annular gap to enhance thermal mass and climate regulation.
- **Installation**: Pre-cast concrete rings sunk into a 5.5 m x 3.5 m excavated pit.

### **Volume Calculation**
- **Inner Volume**: 
  \[
  V = \pi \times r^2 \times h = 3.14 \times (2.5)^2 \times 3 = 58.875 \, \text{m}^3 \approx 58,875 \, \text{liters}
  \]
- **Fish Capacity**: Supports 500–1,000 tilapia (depending on density).
- **Clay Pebble Volume**: Annular gap (5.4 m outer diameter, 5 m inner diameter, 3 m deep):
  \[
  V = \pi \times h \times (R^2 - r^2) = 3.14 \times 3 \times (2.7^2 - 2.5^2) = 3.14 \times 3 \times (7.29 - 6.25) = 9.8 \, \text{m}^3
  \]

---

## **Thermal Mass Contributions**
The reservoir’s thermal mass stabilizes the dome’s temperature, leveraging water, clay pebbles, and surrounding soil.

### **Water**
- **Mass**: \( 58,875 \, \text{liters} \times 1 \, \text{kg/liter} = 58,875 \, \text{kg} \).
- **Specific Heat Capacity**: 4,180 J/kg·°C (1.16 kWh/ton·°C).
- **Heat Capacity**: 
  \[
  C_{\text{water}} = 58,875 \times 1.16 = 68,295 \, \text{kWh/°C} \approx 68.3 \, \text{kWh/°C}
  \]

### **Clay Pebbles**
- **Mass**: \( 9.8 \, \text{m}^3 \times 400 \, \text{kg/m}^3 = 3,920 \, \text{kg} \).
- **Specific Heat Capacity**: 840 J/kg·°C (0.233 kWh/ton·°C).
- **Heat Capacity**: 
  \[
  C_{\text{pebbles}} = 3,920 \times 0.233 = 913.36 \, \text{kWh/°C} \approx 0.914 \, \text{kWh/°C}
  \]

### **Surrounding Soil (0.3 m Shell)**
- **Volume**: Soil from 2.7 m to 3.0 m radius, 3 m deep:
  \[
  V = 3.14 \times 3 \times (3.0^2 - 2.7^2) = 3.14 \times 3 \times (9 - 7.29) = 16.1 \, \text{m}^3
  \]
- **Mass**: \( 16.1 \times 1,500 \, \text{kg/m}^3 = 24,150 \, \text{kg} \).
- **Specific Heat Capacity**: 900 J/kg·°C (0.25 kWh/ton·°C).
- **Heat Capacity**: 
  \[
  C_{\text{soil}} = 24,150 \times 0.25 = 6,037.5 \, \text{kWh/°C} \approx 6.04 \, \text{kWh/°C}
  \]

### **Total Thermal Mass**
\[
C_{\text{total}} = 68.3 + 0.914 + 6.04 = 75.254 \, \text{kWh/°C} \approx 75.3 \, \text{kWh/°C}
\]

---

## **Heat Storage and Release**
- **Heat Stored (Warm Season)**: From 10°C (annual ground average) to 25°C:
  \[
  Q_{\text{stored}} = 75.3 \times (25 - 10) = 75.3 \times 15 = 1,129.5 \, \text{kWh}
  \]
- **Heat Released (Cold Season)**: From 25°C to 20°C:
  \[
  Q_{\text{released}} = 75.3 \times (25 - 20) = 376.5 \, \text{kWh}
  \]
- **Daily Heat Gain Impact**: Summer gain 43.23 kWh/day:
  \[
  \Delta T = \frac{43.23}{75.3} \approx 0.574 \, \text{°C/day}
  \]
  Minimal fluctuation supports 20°C stability.

---

## **Budget**
- **Excavation**: 1,000 euros (5.5 m x 3.5 m pit).
- **Concrete Structure**: 
  - Pre-cast rings and outer shell: 3,000 euros.
  - Waterproofing: 500 euros.
- **Clay Pebbles**: 490 euros (9.8 m³ at 50 euros/m³).
- **Miscellaneous**: 1,000 euros (rebar, labor).
- **Total**: **5,990 euros**.

---

## **Considerations**
- **Thermal Role**: Dominated by water (68.3 kWh/°C), ensuring stability.
- **Structural**: Concrete withstands soil and water pressure.
- **Integration**: Supports floating platform and biofilter.

---

## **Conclusion**
The water reservoir, with a 58,875 L capacity and 75.3 kWh/°C thermal mass, is a cornerstone of the ecosystem, storing 1,129.5 kWh in summer and releasing 376.5 kWh in winter. Costing 5,990 euros, it aligns with the 15,000 euro budget while enabling a stable 20°C environment.