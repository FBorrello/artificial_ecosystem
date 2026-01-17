# Transparent Gored Dome for Artificial Ecosystem

## Overview
The transparent gored dome serves as the primary enclosure for the habitable artificial ecosystem, providing structural support, insulation, and high light transmission. With a diameter of 30 meters and height of 15 meters, it encloses a hemispherical volume that houses the water reservoir, floating platform, and various subsystems. Constructed from 24 gores with ETFE panels and tubular frames, the dome ensures optimal light for photosynthesis.

## Design Specifications
- **Shape**: Hemispherical dome.
- **Dimensions**: Diameter 30 meters, height 15 meters (radius 15 meters). Surface area: 1,414 m². Projected area: 707 m². Volume: 7,069 m³.
- **Gores**: 24 segments, each comprising tubular frames and ETFE panels, subdivided into 8 panels. Gores are arranged radially from the apex, with frames following geodesic lines for optimal load distribution.
- [**Panels**](/docs/idea/dome_panels.md): Double-layer ETFE cushioned panels, 10 layers with varying gores (layers 1-7: 40 gores, layers 8-9: 20 gores), total 320 panels. Each layer spans ~1.5 m height, meridional arc ~2.36 m.
- [**Frames**](/docs/idea/dome_frames.md): Tubular steel or aluminum arches, spaced every 1-2 meters along the gore edges, connected at apex and base.

## Structural Engineering Requirements
### Load Calculations
- **Wind Load**: Assuming location in moderate wind zone (e.g., 50 m/s gust), dynamic pressure ~1.25 kN/m². Total force on dome surface (~1413 m²) ≈ 1766 kN. Frames must withstand this with safety factor of 2.
- **Snow Load**: 1 kN/m², total ~1413 kN.
- **Self-Weight**: ETFE lightweight, frames ~50 kg/m² total.

### Frame Design
- Tubular frames: Circular hollow sections, e.g., 200mm diameter, 10mm wall for base, tapering to 100mm at apex, material high-strength steel (yield 355 MPa) or aluminum alloy (yield 300 MPa). Frames support panel weight and maintain shape.
- Stress analysis: Use finite element modeling to ensure max stress < 0.6 yield. Include buckling analysis for wind and snow loads.
- Connections: Bolted or welded joints at intersections, with gusset plates for reinforcement.

### Foundation
- Base anchored to concrete foundation, resisting wind uplift.

## Material Details
### ETFE Properties
- **Transparency**: 95% light transmission, minimal UV degradation.
- **Tensile Strength**: 50-60 MPa.
- **Thickness**: 100-200 micron per foil layer; cushions inflated to 3-10 cm air gap.
- **Density**: 1.7 g/cm³.
- **Chemical Resistance**: Resistant to acids, bases, UV.
- **Lifespan**: 25+ years.

### Tubular Frames
- Material: Aluminum alloy (lightweight) or galvanized steel.
- Corrosion resistance: Coated for outdoor use.

### Panels
- Double-layer ETFE cushions for insulation and smooth surface.
- Thickness: Inflated to ~5-10 cm air gap, foil 100-200 micron per layer.

## Integration with Ecosystem Systems
- **Energy Systems**: Insulates, allows solar gain.
- **Sensors/Actuators**: Basic monitoring for structural integrity.

## Safety Considerations and Redundancy
- **Structural**: Redundant frames, earthquake-resistant design.
- **Pressure**: Relief valves at 6 bar, overpressure protection.
- **Emergency**: Manual depressurization, evacuation routes.
- **Redundancy**: Backup air storage, multiple compressors.

## Construction Methods and Timeline
- **Fabrication**: Panels pre-assembled, frames welded.
- **Assembly**: On-site erection, inflation testing.
- **Timeline**: 6-12 months, depending on site.

## Cost Estimates
- **Materials**: ETFE cushioned panels ~84,000 € (301 panels), frames ~550,000 €, foundation ~71,000 €, total ~705,000 €.
- **Labor**: Fabrication and installation ~120,000 €.
- **Total**: ~825,000 € (estimate for cushioned ETFE dome with lattice frames; actual costs may vary with location and suppliers).

## Environmental Impact and Sustainability
- **Sustainability**: ETFE recyclable, long lifespan (25+ years), reduces need for replacements.
- **Impact**: High transparency minimizes artificial lighting, cushioned design improves insulation (lower U-value), reducing energy for heating/cooling.
- **Carbon Footprint**: Estimate 60 tons CO2 equivalent (higher due to cushion manufacturing, but offset by energy savings).

## Maintenance and Monitoring
- **Inspection**: Annual pressure checks, frame integrity.
- **Repairs**: Replace panels if punctured.
- **Monitoring**: AI system monitors pressure, alerts for anomalies.

## Future Development
- **Scalability**: Modular design for larger domes.
- **Improvements**: Smart materials, integrated solar cells.

## References
- Prototype requirements document.
- ETFE manufacturer datasheets (e.g., Asahi Glass).