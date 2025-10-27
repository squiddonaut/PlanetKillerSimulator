"""
Meteor Simulator - Visualization Module
Creates visualizations of meteor impact destruction zones
"""

import math


class ImpactVisualizer:
    """Creates text-based visualization of meteor impact zones"""
    
    @staticmethod
    def create_impact_map(city_name, city_info, destruction_zones):
        """
        Create a text-based visualization of impact zones
        
        Args:
            city_name: Name of the city
            city_info: City information dictionary
            destruction_zones: Dictionary of destruction radii
            
        Returns:
            String containing the visualization
        """
        width = 60
        height = 30
        
        # Create empty map
        map_grid = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Center point
        center_x = width // 2
        center_y = height // 2
        
        # Scale factor (km per character)
        max_radius = max(destruction_zones.values())
        if max_radius > 0:
            scale = max_radius / (min(width, height) // 2 - 2)
        else:
            scale = 1
        
        # Draw destruction zones (from outside to inside)
        zones = [
            ('light_damage', '.', destruction_zones.get('light_damage', 0)),
            ('moderate_damage', 'o', destruction_zones.get('moderate_damage', 0)),
            ('severe_damage', 'O', destruction_zones.get('severe_damage', 0)),
            ('total_destruction', '#', destruction_zones.get('total_destruction', 0)),
            ('fireball', '*', destruction_zones.get('fireball', 0))
        ]
        
        for zone_name, char, radius in zones:
            if radius > 0:
                radius_chars = int(radius / scale)
                for y in range(height):
                    for x in range(width):
                        dx = x - center_x
                        dy = (y - center_y) * 2  # Adjust for character aspect ratio
                        distance = math.sqrt(dx**2 + dy**2)
                        if distance <= radius_chars:
                            map_grid[y][x] = char
        
        # Mark impact point
        if 0 <= center_y < height and 0 <= center_x < width:
            map_grid[center_y][center_x] = 'X'
        
        # Convert to string
        map_str = '\n'.join([''.join(row) for row in map_grid])
        
        # Create legend
        legend = f"""
Impact Location: {city_name} ({city_info['country']})
Coordinates: {city_info['latitude']:.2f}°N, {abs(city_info['longitude']):.2f}°{'W' if city_info['longitude'] < 0 else 'E'}
Population: {city_info['population']:,} (Metro: {city_info['metro_population']:,})

Legend:
  X = Impact Point
  * = Fireball ({destruction_zones.get('fireball', 0):.1f} km)
  # = Total Destruction ({destruction_zones.get('total_destruction', 0):.1f} km)
  O = Severe Damage ({destruction_zones.get('severe_damage', 0):.1f} km)
  o = Moderate Damage ({destruction_zones.get('moderate_damage', 0):.1f} km)
  . = Light Damage ({destruction_zones.get('light_damage', 0):.1f} km)
"""
        
        return map_str + '\n' + legend
    
    @staticmethod
    def format_impact_summary(impact_data):
        """
        Format impact data into a readable summary
        
        Args:
            impact_data: Dictionary of impact calculations
            
        Returns:
            Formatted string summary
        """
        summary = f"""
{'=' * 70}
METEOR IMPACT ANALYSIS
{'=' * 70}

METEOR PROPERTIES:
  Diameter:        {impact_data['diameter_m']:.1f} meters
  Velocity:        {impact_data['velocity_ms']:.1f} m/s ({impact_data['velocity_ms'] * 3.6:.1f} km/h)
  Material:        {impact_data['material'].title()}
  Density:         {impact_data['density_kgm3']:,.0f} kg/m³
  Mass:            {impact_data['mass_kg']:.2e} kg ({impact_data['mass_kg']/1000:.2e} tonnes)

IMPACT EFFECTS:
  Kinetic Energy:  {impact_data['energy_joules']:.2e} Joules
  TNT Equivalent:  {impact_data['tnt_equivalent_kt']:.2f} kilotons
  Crater Diameter: {impact_data['crater_diameter_m']:.1f} meters

DESTRUCTION ZONES:
  Fireball Radius:         {impact_data['destruction_zones']['fireball']:.2f} km
  Total Destruction:       {impact_data['destruction_zones']['total_destruction']:.2f} km
  Severe Damage:           {impact_data['destruction_zones']['severe_damage']:.2f} km
  Moderate Damage:         {impact_data['destruction_zones']['moderate_damage']:.2f} km
  Light Damage:            {impact_data['destruction_zones']['light_damage']:.2f} km

{'=' * 70}
"""
        return summary
    
    @staticmethod
    def format_comparison(impact_data):
        """
        Create comparison with known events
        
        Args:
            impact_data: Dictionary of impact calculations
            
        Returns:
            Formatted comparison string
        """
        tnt_kt = impact_data['tnt_equivalent_kt']
        
        comparisons = []
        
        # Hiroshima bomb: ~15 kilotons
        if tnt_kt >= 0.01:
            hiroshima_multiple = tnt_kt / 15
            comparisons.append(f"  ≈ {hiroshima_multiple:.2f}x Hiroshima atomic bomb")
        
        # Tunguska event: ~10-15 megatons
        tunguska_kt = 12000  # 12 megatons
        if tnt_kt >= 100:
            tunguska_multiple = tnt_kt / tunguska_kt
            comparisons.append(f"  ≈ {tunguska_multiple:.2f}x Tunguska event (1908)")
        
        # Chicxulub impact (dinosaur extinction): ~100 million megatons
        chicxulub_kt = 100_000_000_000  # 100 million megatons
        if tnt_kt >= 1_000_000:
            chicxulub_multiple = tnt_kt / chicxulub_kt
            comparisons.append(f"  ≈ {chicxulub_multiple:.2e}x Chicxulub impact (dinosaurs)")
        
        if comparisons:
            comparison_str = "\nCOMPARISONS:\n" + '\n'.join(comparisons) + '\n'
        else:
            comparison_str = "\nCOMPARISONS:\n  Impact too small for meaningful comparisons\n"
        
        return comparison_str
