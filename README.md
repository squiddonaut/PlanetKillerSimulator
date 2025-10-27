# Planet Killer Simulator

A Python-based meteor impact simulator that calculates and visualizes the destructive effects of asteroid/comet strikes on major Earth cities.

## Features

- **Customizable Meteor Parameters**: Specify diameter, velocity, and material composition
- **Multiple Material Types**: Choose from Iron, Stone, Ice, and Nickel-Iron asteroids
- **Major Cities Database**: Target 20+ major world cities
- **Physics-Based Calculations**: Accurate impact energy and destruction zone calculations
- **Visual Impact Maps**: ASCII-based visualization of destruction zones
- **Comparative Analysis**: Compare impact energy to historical events (Hiroshima, Tunguska, etc.)

## Installation

### Prerequisites
- Python 3.6 or higher

### Setup
```bash
# Clone the repository
git clone https://github.com/squiddonaut/PlanetKillerSimulator.git
cd PlanetKillerSimulator

# No external dependencies required - uses Python standard library only!
```

## Usage

### Running the Simulator

```bash
python simulator.py
```

### Interactive Mode

The simulator will guide you through:

1. **Meteor Parameters**:
   - Diameter (in meters, e.g., 10-1000m)
   - Impact velocity (in m/s, typical range: 11,000-72,000 m/s)
   - Material type (Iron, Stone, Ice, Nickel-Iron)

2. **Target Selection**:
   - Choose from 20+ major world cities
   - Includes cities like New York, Tokyo, London, Paris, etc.

3. **Results**:
   - Kinetic energy calculation
   - TNT equivalent
   - Crater diameter estimation
   - Destruction zone radii
   - ASCII visualization map
   - Comparisons to historical events

### Example Session

```
METEOR PARAMETERS:
Enter meteor diameter in meters (e.g., 10-1000): 50
Enter impact velocity in m/s (typical: 11,000-72,000): 20000

Select material: Iron

Select target city: New York

IMPACT ANALYSIS:
  Kinetic Energy:  3.24e+16 Joules
  TNT Equivalent:  7,751.20 kilotons
  Crater Diameter: 1,234.5 meters
  
DESTRUCTION ZONES:
  Fireball Radius:         0.89 km
  Total Destruction:       2.20 km
  Severe Damage:           4.41 km
  Moderate Damage:         8.82 km
  Light Damage:            17.64 km
```

## Testing

Run the test suite to validate physics calculations:

```bash
python -m unittest test_simulator.py
```

Or run with verbose output:

```bash
python -m unittest test_simulator.py -v
```

## Project Structure

```
PlanetKillerSimulator/
├── simulator.py          # Main CLI interface
├── meteor_physics.py     # Physics calculations and impact modeling
├── cities.py            # Database of major world cities
├── visualization.py     # Impact visualization and formatting
├── test_simulator.py    # Unit tests
└── README.md           # This file
```

## Physics Model

The simulator uses simplified but physics-based models:

### Mass Calculation
```
Volume = (4/3) × π × r³
Mass = Volume × Density
```

### Kinetic Energy
```
KE = 0.5 × Mass × Velocity²
```

### Crater Formation
Based on empirical scaling laws from impact crater studies.

### Destruction Zones
Calculated using energy scaling similar to nuclear weapon effects, adapted for meteor impacts.

## Material Properties

| Material    | Density (kg/m³) | Description              |
|-------------|-----------------|--------------------------|
| Iron        | 7,870           | Dense metallic asteroid  |
| Stone       | 3,300           | Rocky asteroid           |
| Ice         | 917             | Icy comet                |
| Nickel-Iron | 8,000           | Dense metallic asteroid  |

## Available Cities

The simulator includes 20 major world cities across all continents:
- **Americas**: New York, Los Angeles, Toronto, Mexico City, São Paulo, Buenos Aires
- **Europe**: London, Paris, Moscow, Berlin, Istanbul
- **Asia**: Tokyo, Beijing, Mumbai, Seoul, Hong Kong, Singapore, Dubai
- **Middle East/Africa**: Cairo
- **Oceania**: Sydney

## Limitations

- Simplified atmospheric entry effects (no fragmentation modeling)
- Does not account for impact angle
- Simplified crater formation models
- Does not model seismic effects or tsunamis
- Destruction zones are approximations based on energy scaling

