# In-Depth Report: Transparent Dome for Artificial Ecosystem Prototype

This report details the transparent dome’s design, insulation, thermal performance, and cost, incorporating perimeter walls, a revised internal pressure of 1 bar, and a large access door at the base. It ensures structural integrity, light transmission, a stable 20°C year-round, and air supply for pneumatic pump cycles.

---

## **Design Specifications**
- **Shape**: Non-geodesic, hemispherical, 6-meter diameter.
- **Panels**: Pressurized (1 bar gauge), transparent, box-like, self-sustaining, with quick-release connections and perimeter walls.
- **Thickness**: Base 55 cm (4 inner layers), halving to 27.5 cm at top (1 inner layer).
- **Door**: 2 m x 2 m at base row, reducing base panels from 16 to 12.
- **Role**: Structural support, compressed air reservoir, insulation, access.

---

## **Design and Implementation**
### **Structure**
- **Material**: Polycarbonate sheets.
- **Base Panels**: 55 cm thick, 5 layers (2 mm each, 4 air gaps, ~13.5 cm each), 4 perimeter walls (2 mm thick).
- **Top Panels**: 27.5 cm thick, 2 layers (2 mm each, 1 air gap, ~27.1 cm), 1 perimeter wall (2 mm thick).
- **Construction**: 36 panels (1.41 m² each, ~1.19 m x 1.19 m), tapering in 7–8 rows; door replaces 4 base panels.
- **Door**: 2 m x 2 m, 10 cm air gap, hinged with pressure-tight latches.

### **Surface Area**
- **Hemisphere**: 
  \[
  A = 2\pi r^2 = 2 \times 3.14 \times 3^2 = 56.52 \, \text{m}^2
  \]
- **Adjusted**: 36 panels (50.76 m²) + door (4 m²) = 54.76 m².

---

## **Thermal Insulation (U-Value)**
### **Calculation**
1. **Base Panels (55 cm, 4 inner layers)**:
   - Plastic (5 layers, 2 mm each, 1 cm total): \( R = \frac{0.01}{0.2} = 0.05 \, \text{m}^2·\text{K/W} \).
   - Air Gaps (4 x 13.5 cm = 54 cm): \( R = \frac{0.54}{0.026} = 20.77 \, \text{m}^2·\text{K/W} \).
   - Total R: \( 0.05 + 20.77 = 20.82 \, \text{m}^2·\text{K/W} \).
   - U-Value: \( U = \frac{1}{20.82} \approx 0.048 \, \text{W/m}^2·\text{K} \).

2. **Top Panels (27.5 cm, 1 inner layer)**:
   - Plastic (2 layers, 4 mm total): \( R = \frac{0.004}{0.2} = 0.02 \, \text{m}^2·\text{K/W} \).
   - Air Gap (27.1 cm): \( R = \frac{0.271}{0.026} = 10.42 \, \text{m}^2·\text{K/W} \).
   - Total R: \( 0.02 + 10.42 = 10.44 \, \text{m}^2·\text{K/W} \).
   - U-Value: \( U = \frac{1}{10.44} \approx 0.096 \, \text{W/m}^2·\text{K} \).

3. **Average U-Value**: 
   \[
   U_{\text{avg}} = \frac{0.048 + 0.096}{2} = 0.072 \, \text{W/m}^2·\text{K}
   \]
   Adjusted to **0.1 W/m²·K** for convection and seams.

- **Door**: 10 cm air gap, U ~0.25 W/m²·K, minor impact on average.

---

## **Heat Loss**
- **Conditions**: 20°C inside, 5°C outside (\( \Delta T = 15°C \)).
- **Heat Loss Rate (Panels)**: 
  \[
  0.1 \times 50.76 \times 15 = 76.14 \, \text{W}
  \]
- **Heat Loss Rate (Door)**: 
  \[
  0.25 \times 4 \times 15 = 15 \, \text{W}
  \]
- **Total**: \( 76.14 + 15 = 91.14 \, \text{W} = 0.09114 \, \text{kW} \).
- **Daily Heat Loss**: 
  \[
  0.09114 \times 24 = 2.187 \, \text{kWh/day}
  \]
- **Cold Season (182 days)**: 
  \[
  2.187 \times 182 = 398 \, \text{kWh}
  \]

---

## **Solar Heat Gain**
- **Projected Area**: \( \pi \times 3^2 = 28.3 \, \text{m}^2 \).
- **Transmission**: \( e^{-0.7675 \cdot r} \):
  \[
  Q_{\text{solar, daily}} = 5.5 \times 2\pi \times 1.137 = 39.3 \, \text{kWh/day} \, \text{(summer)}
  \]
- **Warm Season (183 days)**: 
  \[
  Q_{\text{solar, warm}} = 39.3 \times 183 = 7,194 \, \text{kWh}
  \]
- **Winter (1 kWh/m²/day)**: 
  \[
  Q_{\text{solar, daily}} = 1 \times 28.3 \times 0.35 = 9.91 \, \text{kWh/day}
  \]
  \[
  Q_{\text{solar, cold}} = 9.91 \times 182 = 1,804 \, \text{kWh}
  \]

---

## **Annual Heat Balance**
- **Warm Season**:
  - Solar Gain: 7,194 kWh.
  - Heat Loss (17.5°C outside): \( 0.1 \times 50.76 \times 2.5 \times 24 \times 183 / 1,000 = 56 \, \text{kWh} \) + \( 0.25 \times 4 \times 2.5 \times 24 \times 183 / 1,000 = 11 \, \text{kWh} \) = 67 kWh.
  - Net: 7,127 kWh.
  - Stored: 1,129.5 kWh (75.3 kWh/°C, 10°C to 25°C).
  - Excess Vented: 5,997.5 kWh.
- **Cold Season**:
  - Heat Loss: 398 kWh.
  - Solar Gain: 1,804 kWh.
  - Surplus: 1,406 kWh.
  - Released: 376.5 kWh (25°C to 20°C).

---

## **Pressure and Pump Cycle Analysis**
### **Pressure at 1 Bar**
- **Original Pressure**: 2 bar gauge (200 kPa).
- **Revised Pressure**: 1 bar gauge (100 kPa).
- **Benefits**:
  - **Construction**: Stress reduced by 50% (~59 MPa vs. 118 MPa), using 2 mm sheets and walls without ribs.
  - **Assembly**: Simpler sealing, fabrication cost down to 15 euros/panel.
  - **Material**: Perimeter walls 2 mm (3.2054 kg vs. 4.808 kg), cost from 19.23 to 12.82 euros/panel.
  - **Total Cost per Panel**: \( 37.97 + 12.82 + 15 + 15 = 80.79 \, \text{euros} \).

### **Pump Cycles Before 0.5 Bar Threshold**
- **Air Reservoir Volume**: 21.34 m³ (36 panels at 20.94 m³ + door at 0.4 m³).
- **Initial Pressure**: 1 bar gauge = 201.3 kPa absolute.
- **Initial Air Mass**: 
  \[
  m = \frac{201,300 \times 21.34}{287 \times 293} \approx 51.06 \, \text{kg}
  \]
- **Threshold Pressure**: 0.5 bar gauge = 151.3 kPa absolute.
- **Threshold Mass**: 
  \[
  m_{\text{threshold}} = \frac{151,300 \times 21.34}{287 \times 293} \approx 38.38 \, \text{kg}
  \]
- **Available Mass**: \( 51.06 - 38.38 = 12.68 \, \text{kg} \).
- **Mass per Cycle**: Pump (0.58905 m³, 35 kPa gauge = 136.3 kPa absolute):
  \[
  m_{\text{cycle}} = \frac{136,300 \times 0.58905}{287 \times 293} \approx 0.955 \, \text{kg}
  \]
- **Cycles**: 
  \[
  N = \frac{12.68}{0.955} \approx 13.28
  \]
  - **Result**: **13 cycles**.

---

## **Budget**
- **Revised Cost**: **3,057 euros**.
- **Breakdown**: 
  - **Panels**: 36 panels, 1.41 m² each.
    - Polycarbonate Sheets: 37.97 euros/panel (9.492 kg at 4 euros/kg).
    - Perimeter Walls (2 mm): 12.82 euros/panel (3.2054 kg at 4 euros/kg).
    - Fittings: 15 euros/panel.
    - Fabrication: 15 euros/panel.
    - Total per panel: \( 80.79 \, \text{euros} \).
    - Subtotal: \( 80.79 \times 36 = 2,908.44 \, \text{euros} \).
  - **Door**: 2 m x 2 m, 10 cm air gap.
    - Polycarbonate: 48 euros (12 kg at 4 euros/kg).
    - Fittings/Fabrication: 100 euros.
    - Subtotal: 148 euros.
  - **Total**: \( 2,908.44 + 148 = 3,056.44 \, \text{euros} \approx 3,057 \, \text{euros} \).

---

## **Conclusion**
The dome, with a U-value of 0.1 W/m²·K, perimeter walls, and a 2 m x 2 m door, loses 398 kWh in winter, covered by 376.5 kWh from thermal mass and 1,804 kWh solar gain. Summer storage of 1,129.5 kWh ensures 20°C stability. At 1 bar pressure, it supports 13 pump cycles before dropping below 0.5 bar, costing 3,057 euros for 36 panels and a door, fitting within the 15,000 euro budget with optimized design.