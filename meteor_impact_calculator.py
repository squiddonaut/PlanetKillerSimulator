"""
Meteor Impact Calculator for Planet Killer Simulator
A single script to calculate meteor impact effects for use in Godot game.
Returns all values in a clean dictionary format for easy integration.
"""

import math


def calculate_meteor_impact(
    meteor_diameter=1000.0,  # meters
    meteor_velocity=20000.0,  # m/s
    meteor_density=3000.0,  # kg/m³
    impact_angle=45.0,  # degrees
    target_surface_type='land',
    impact_latitude=0.0,
    impact_longitude=0.0
):
    """
    Calculate all meteor impact effects and return as a dictionary.
    
    Parameters:
    -----------
    meteor_diameter : float
        Diameter of the meteor in meters (default: 1000m = 1km)
    meteor_velocity : float
        Impact velocity in m/s (default: 20,000 m/s)
    meteor_density : float
        Density in kg/m³ (default: 3000 for stone meteor)
        Common values: Stone=3000, Iron=7800, Ice=917
    impact_angle : float
        Impact angle in degrees, 0=horizontal, 90=vertical (default: 45)
    target_surface_type : str
        'land', 'ocean', 'desert', 'ice' (default: 'land')
    impact_latitude : float
        Latitude of impact -90 to 90 (default: 0)
    impact_longitude : float
        Longitude of impact -180 to 180 (default: 0)
    
    Returns:
    --------
    dict : All impact calculations ready for Godot visualization
    """
    
    # Calculate meteor mass
    meteor_radius = meteor_diameter / 2.0
    meteor_volume = (4.0 / 3.0) * math.pi * (meteor_radius ** 3)
    meteor_mass = meteor_volume * meteor_density
    
    # Calculate kinetic energy
    kinetic_energy = 0.5 * meteor_mass * (meteor_velocity ** 2)
    energy_megatons = kinetic_energy / 4.184e15  # Convert to megatons TNT
    
    # Impact angle correction factor
    angle_rad = math.radians(impact_angle)
    angle_correction = math.sin(angle_rad)
    
    # CRATER CALCULATIONS
    # Using simplified Schmidt-Holsapple scaling
    gravity = 9.81  # m/s²
    target_density = 2500.0  # kg/m³ for rock
    if target_surface_type == 'ocean':
        target_density = 1025.0
    elif target_surface_type == 'ice':
        target_density = 917.0
    
    # Crater diameter (simplified scaling law)
    crater_diameter = 2.0 * (meteor_diameter ** 0.78) * ((meteor_velocity / 1000.0) ** 0.44) * angle_correction
    crater_depth = crater_diameter / 5.0  # Typical depth/diameter ratio
    crater_volume = (math.pi / 3.0) * (crater_diameter / 2.0) ** 2 * crater_depth
    
    # Convert to km for easier visualization
    crater_diameter_km = crater_diameter / 1000.0
    crater_depth_km = crater_depth / 1000.0
    crater_volume_km3 = crater_volume / 1e9
    
    # THERMAL EFFECTS
    # Approximately 30-50% of kinetic energy converts to heat
    thermal_energy = kinetic_energy * 0.4
    
    # Fireball radius (empirical formula)
    fireball_radius = 0.28 * (energy_megatons ** 0.33) * 1000.0  # meters
    fireball_radius_km = fireball_radius / 1000.0
    
    # Impact temperature (simplified - actual is more complex)
    impact_temperature = 5000.0 + (energy_megatons ** 0.5) * 500.0  # Kelvin
    
    # DESTRUCTION ZONES (for game visualization)
    # Total destruction radius
    total_destruction_radius_km = 2.0 * fireball_radius_km
    
    # Severe damage (air blast) - scales with energy
    severe_damage_radius_km = 5.0 * (energy_megatons ** 0.33)
    
    # Moderate damage radius
    moderate_damage_radius_km = 10.0 * (energy_megatons ** 0.33)
    
    # Light damage / blast wave radius
    light_damage_radius_km = 20.0 * (energy_megatons ** 0.33)
    
    # DUST CLOUD AND IMPACT WINTER
    # Calculate ejecta mass (simplified - typically 10-100x crater volume)
    ejecta_factor = 30.0  # Average multiplier
    ejecta_volume = crater_volume * ejecta_factor
    dust_ejected_mass = ejecta_volume * target_density
    
    # Stratospheric dust (only fine particles reach stratosphere)
    stratosphere_fraction = 0.01 if energy_megatons < 100 else 0.1
    if energy_megatons > 10000:
        stratosphere_fraction = 0.3
    stratosphere_dust_mass = dust_ejected_mass * stratosphere_fraction
    
    # Dust cloud coverage area
    if energy_megatons < 100:
        dust_coverage_km2 = energy_megatons * 10000
        affected_hemisphere = 'regional'
    elif energy_megatons < 10000:
        dust_coverage_km2 = energy_megatons * 50000
        affected_hemisphere = 'northern' if impact_latitude > 0 else 'southern'
    else:
        dust_coverage_km2 = 510000000  # Entire Earth surface
        affected_hemisphere = 'global'
    
    # Impact winter duration (in years)
    if stratosphere_dust_mass < 1e12:
        impact_winter_duration = 0.0
    elif stratosphere_dust_mass < 1e14:
        impact_winter_duration = 0.5
    elif stratosphere_dust_mass < 1e15:
        impact_winter_duration = 2.0
    else:
        impact_winter_duration = 5.0 + math.log10(stratosphere_dust_mass / 1e15)
    
    # Global temperature drop (Celsius)
    if stratosphere_dust_mass < 1e12:
        temperature_drop = 0.0
    else:
        temperature_drop = min(25.0, 2.0 * math.log10(stratosphere_dust_mass / 1e12))
    
    # Determine impact severity category
    if energy_megatons < 1:
        severity = 'minor'
    elif energy_megatons < 100:
        severity = 'significant'
    elif energy_megatons < 10000:
        severity = 'catastrophic'
    elif energy_megatons < 100000000:
        severity = 'extinction-level'
    else:
        severity = 'planet-killer'
    
    # Return all results as a clean dictionary
    return {
        # Input parameters (echo back for reference)
        'input': {
            'meteor_diameter_m': meteor_diameter,
            'meteor_diameter_km': meteor_diameter / 1000.0,
            'meteor_velocity_ms': meteor_velocity,
            'meteor_velocity_kms': meteor_velocity / 1000.0,
            'meteor_density': meteor_density,
            'meteor_mass_kg': meteor_mass,
            'impact_angle_deg': impact_angle,
            'target_surface_type': target_surface_type,
            'impact_latitude': impact_latitude,
            'impact_longitude': impact_longitude
        },
        
        # Crater dimensions
        'crater': {
            'diameter_km': crater_diameter_km,
            'depth_km': crater_depth_km,
            'volume_km3': crater_volume_km3
        },
        
        # Energy and heat
        'energy': {
            'kinetic_energy_joules': kinetic_energy,
            'kinetic_energy_megatons': energy_megatons,
            'thermal_energy_joules': thermal_energy,
            'impact_temperature_kelvin': impact_temperature,
            'impact_temperature_celsius': impact_temperature - 273.15,
            'fireball_radius_km': fireball_radius_km
        },
        
        # Destruction zones (for visualizing on globe)
        'destruction_zones': {
            'total_destruction_km': total_destruction_radius_km,
            'severe_damage_km': severe_damage_radius_km,
            'moderate_damage_km': moderate_damage_radius_km,
            'light_damage_km': light_damage_radius_km
        },
        
        # Dust cloud and impact winter
        'dust_effects': {
            'dust_ejected_mass_kg': dust_ejected_mass,
            'stratosphere_dust_mass_kg': stratosphere_dust_mass,
            'dust_cloud_coverage_km2': dust_coverage_km2,
            'affected_hemisphere': affected_hemisphere,
            'impact_winter_duration_years': impact_winter_duration,
            'global_temperature_drop_celsius': temperature_drop
        },
        
        # Overall assessment
        'assessment': {
            'severity': severity,
            'is_extinction_event': energy_megatons > 10000,
            'is_global_catastrophe': affected_hemisphere == 'global'
        }
    }


def format_results(results):
    """Pretty print results for testing."""
    print("\n" + "="*60)
    print("METEOR IMPACT SIMULATION RESULTS")
    print("="*60)
    
    print(f"\nINPUT PARAMETERS:")
    print(f"  Meteor Diameter: {results['input']['meteor_diameter_km']:.2f} km")
    print(f"  Meteor Velocity: {results['input']['meteor_velocity_kms']:.2f} km/s")
    print(f"  Meteor Mass: {results['input']['meteor_mass_kg']:.2e} kg")
    print(f"  Impact Angle: {results['input']['impact_angle_deg']}°")
    print(f"  Surface Type: {results['input']['target_surface_type']}")
    
    print(f"\nCRATER:")
    print(f"  Diameter: {results['crater']['diameter_km']:.2f} km")
    print(f"  Depth: {results['crater']['depth_km']:.2f} km")
    print(f"  Volume: {results['crater']['volume_km3']:.2f} km³")
    
    print(f"\nENERGY & HEAT:")
    print(f"  Impact Energy: {results['energy']['kinetic_energy_megatons']:.2f} megatons TNT")
    print(f"  Thermal Energy: {results['energy']['thermal_energy_joules']:.2e} Joules")
    print(f"  Impact Temperature: {results['energy']['impact_temperature_celsius']:.0f}°C")
    print(f"  Fireball Radius: {results['energy']['fireball_radius_km']:.2f} km")
    
    print(f"\nDESTRUCTION ZONES:")
    print(f"  Total Destruction: {results['destruction_zones']['total_destruction_km']:.2f} km radius")
    print(f"  Severe Damage: {results['destruction_zones']['severe_damage_km']:.2f} km radius")
    print(f"  Moderate Damage: {results['destruction_zones']['moderate_damage_km']:.2f} km radius")
    print(f"  Light Damage: {results['destruction_zones']['light_damage_km']:.2f} km radius")
    
    print(f"\nDUST CLOUD & IMPACT WINTER:")
    print(f"  Dust Ejected: {results['dust_effects']['dust_ejected_mass_kg']:.2e} kg")
    print(f"  Stratospheric Dust: {results['dust_effects']['stratosphere_dust_mass_kg']:.2e} kg")
    print(f"  Coverage Area: {results['dust_effects']['dust_cloud_coverage_km2']:.2e} km²")
    print(f"  Affected Region: {results['dust_effects']['affected_hemisphere']}")
    print(f"  Impact Winter Duration: {results['dust_effects']['impact_winter_duration_years']:.1f} years")
    print(f"  Global Temperature Drop: {results['dust_effects']['global_temperature_drop_celsius']:.1f}°C")
    
    print(f"\nASSESSMENT:")
    print(f"  Severity: {results['assessment']['severity'].upper()}")
    print(f"  Extinction Event: {'YES' if results['assessment']['is_extinction_event'] else 'NO'}")
    print(f"  Global Catastrophe: {'YES' if results['assessment']['is_global_catastrophe'] else 'NO'}")
    print("="*60 + "\n")


# Example usage and testing
if __name__ == "__main__":
    print("METEOR IMPACT CALCULATOR - Test Examples")
    
    # Example 1: Small meteor (similar to Chelyabinsk 2013)
    print("\n### Example 1: Small Meteor (Chelyabinsk-like) ###")
    results1 = calculate_meteor_impact(
        meteor_diameter=20,  # 20 meters
        meteor_velocity=19000,
        meteor_density=3000,
        impact_angle=20,
        target_surface_type='land'
    )
    format_results(results1)
    
    # Example 2: Medium meteor (Tunguska-like)
    print("\n### Example 2: Medium Meteor (Tunguska-like) ###")
    results2 = calculate_meteor_impact(
        meteor_diameter=60,  # 60 meters
        meteor_velocity=15000,
        meteor_density=3000,
        impact_angle=30,
        target_surface_type='land'
    )
    format_results(results2)
    
    # Example 3: Large meteor (Chicxulub-like - dinosaur killer)
    print("\n### Example 3: Dinosaur Killer (Chicxulub-like) ###")
    results3 = calculate_meteor_impact(
        meteor_diameter=10000,  # 10 km
        meteor_velocity=20000,
        meteor_density=3000,
        impact_angle=45,
        target_surface_type='land',
        impact_latitude=21.3
    )
    format_results(results3)
    
    # Example 4: Planet Killer
    print("\n### Example 4: PLANET KILLER ###")
    results4 = calculate_meteor_impact(
        meteor_diameter=100000,  # 100 km
        meteor_velocity=25000,
        meteor_density=3000,
        impact_angle=90,
        target_surface_type='ocean'
    )
    format_results(results4)
    
    # Show how to access individual values for Godot
    print("\n" + "="*60)
    print("HOW TO USE IN GODOT:")
    print("="*60)
    print("""
# In Godot, you can call this Python script and access values like:

results = calculate_meteor_impact(
    meteor_diameter=1000,
    meteor_velocity=20000,
    meteor_density=3000,
    impact_angle=45
)

# Access specific values:
crater_size = results['crater']['diameter_km']
energy = results['energy']['kinetic_energy_megatons']
fireball = results['energy']['fireball_radius_km']
total_destruction = results['destruction_zones']['total_destruction_km']
severity = results['assessment']['severity']

# Use these values to visualize on your globe!
    """