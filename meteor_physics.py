"""
Meteor Physics Module
Calculates impact energy and destruction zones for meteor strikes
"""

import math


class MeteorMaterial:
    """Defines material properties for different meteor types"""
    
    MATERIALS = {
        'iron': {
            'density': 7870,  # kg/m³
            'name': 'Iron',
            'description': 'Dense metallic asteroid'
        },
        'stone': {
            'density': 3300,  # kg/m³
            'name': 'Stone',
            'description': 'Rocky asteroid'
        },
        'ice': {
            'density': 917,   # kg/m³
            'name': 'Ice',
            'description': 'Icy comet'
        },
        'nickel_iron': {
            'density': 8000,  # kg/m³
            'name': 'Nickel-Iron',
            'description': 'Dense metallic asteroid with nickel'
        }
    }
    
    @classmethod
    def get_density(cls, material_type):
        """Get density for a material type"""
        if material_type.lower() in cls.MATERIALS:
            return cls.MATERIALS[material_type.lower()]['density']
        return cls.MATERIALS['stone']['density']  # Default to stone
    
    @classmethod
    def get_all_materials(cls):
        """Get list of all available materials"""
        return list(cls.MATERIALS.keys())
    
    @classmethod
    def get_material_info(cls, material_type):
        """Get detailed info about a material"""
        return cls.MATERIALS.get(material_type.lower(), cls.MATERIALS['stone'])


class ImpactCalculator:
    """Calculates meteor impact effects"""
    
    # Physical constants
    TNT_ENERGY = 4.184e12  # Joules per kiloton of TNT
    
    @staticmethod
    def calculate_mass(diameter, material_density):
        """
        Calculate meteor mass from diameter and density
        
        Args:
            diameter: Meteor diameter in meters
            material_density: Material density in kg/m³
            
        Returns:
            Mass in kilograms
        """
        radius = diameter / 2
        volume = (4/3) * math.pi * (radius ** 3)
        mass = volume * material_density
        return mass
    
    @staticmethod
    def calculate_kinetic_energy(mass, velocity):
        """
        Calculate kinetic energy of meteor
        
        Args:
            mass: Mass in kg
            velocity: Velocity in m/s
            
        Returns:
            Kinetic energy in Joules
        """
        return 0.5 * mass * (velocity ** 2)
    
    @staticmethod
    def energy_to_tnt_kilotons(energy_joules):
        """
        Convert energy to TNT equivalent in kilotons
        
        Args:
            energy_joules: Energy in Joules
            
        Returns:
            Energy in kilotons of TNT
        """
        return energy_joules / ImpactCalculator.TNT_ENERGY
    
    @staticmethod
    def calculate_crater_diameter(energy_joules):
        """
        Estimate crater diameter based on impact energy
        Uses empirical formula: D = 1.8 * E^0.25 (simplified)
        
        Args:
            energy_joules: Impact energy in Joules
            
        Returns:
            Crater diameter in meters
        """
        # Simplified crater scaling law
        energy_megatons = energy_joules / (4.184e15)  # Convert to megatons
        diameter = 1800 * (energy_megatons ** 0.25)  # Empirical formula
        return diameter
    
    @staticmethod
    def calculate_destruction_radius(energy_joules):
        """
        Calculate destruction radius for different levels of damage
        
        Args:
            energy_joules: Impact energy in Joules
            
        Returns:
            Dictionary with destruction radii in km for different damage levels
        """
        energy_megatons = energy_joules / (4.184e15)
        
        # Empirical formulas for different damage zones (simplified)
        # Based on nuclear weapon effects scaled for meteor impacts
        
        return {
            'total_destruction': math.sqrt(energy_megatons) * 2.5,      # km
            'severe_damage': math.sqrt(energy_megatons) * 5.0,          # km
            'moderate_damage': math.sqrt(energy_megatons) * 10.0,       # km
            'light_damage': math.sqrt(energy_megatons) * 20.0,          # km
            'fireball': (energy_megatons ** 0.4) * 0.5                  # km
        }
    
    @staticmethod
    def calculate_impact_effects(diameter, velocity, material):
        """
        Calculate all impact effects for a meteor strike
        
        Args:
            diameter: Meteor diameter in meters
            velocity: Impact velocity in m/s
            material: Material type string
            
        Returns:
            Dictionary with all calculated impact effects
        """
        density = MeteorMaterial.get_density(material)
        mass = ImpactCalculator.calculate_mass(diameter, density)
        energy = ImpactCalculator.calculate_kinetic_energy(mass, velocity)
        tnt_kilotons = ImpactCalculator.energy_to_tnt_kilotons(energy)
        crater_diameter = ImpactCalculator.calculate_crater_diameter(energy)
        destruction_radii = ImpactCalculator.calculate_destruction_radius(energy)
        
        return {
            'diameter_m': diameter,
            'velocity_ms': velocity,
            'material': material,
            'density_kgm3': density,
            'mass_kg': mass,
            'energy_joules': energy,
            'tnt_equivalent_kt': tnt_kilotons,
            'crater_diameter_m': crater_diameter,
            'destruction_zones': destruction_radii
        }

# Add this function to meteor_physics.py

import math

def calculate_casualties(destruction_zones, city_density):
    """
    Calculate estimated casualties based on destruction zones and city population density.
    
    Args:
        destruction_zones: dict with keys 'fireball', 'total_destruction', 
                          'severe_damage', 'moderate_damage', 'light_damage' (radii in km)
        city_density: population density in people per km²
    
    Returns:
        dict with casualty estimates for each zone
    """
    
    def calculate_zone_area(outer_radius, inner_radius=0):
        """Calculate area of an annular zone."""
        return math.pi * (outer_radius**2 - inner_radius**2)
    
    # Mortality rates for each zone
    mortality_rates = {
        'fireball': 1.00,           # 100% fatality
        'total_destruction': 0.98,   # 98% fatality
        'severe_damage': 0.70,       # 70% fatality
        'moderate_damage': 0.30,     # 30% fatality
        'light_damage': 0.05         # 5% fatality
    }
    
    # Injury rates for survivors in each zone
    injury_rates = {
        'fireball': 0.00,            # No survivors to injure
        'total_destruction': 0.95,   # 95% of survivors injured
        'severe_damage': 0.85,       # 85% of survivors injured
        'moderate_damage': 0.60,     # 60% of survivors injured
        'light_damage': 0.40         # 40% of survivors injured
    }
    
    zones = [
        ('fireball', destruction_zones['fireball'], 0),
        ('total_destruction', destruction_zones['total_destruction'], destruction_zones['fireball']),
        ('severe_damage', destruction_zones['severe_damage'], destruction_zones['total_destruction']),
        ('moderate_damage', destruction_zones['moderate_damage'], destruction_zones['severe_damage']),
        ('light_damage', destruction_zones['light_damage'], destruction_zones['moderate_damage'])
    ]
    
    casualties = {
        'deaths_by_zone': {},
        'injuries_by_zone': {},
        'total_deaths': 0,
        'total_injuries': 0,
        'total_affected': 0
    }
    
    for zone_name, outer_radius, inner_radius in zones:
        # Calculate area of this zone
        zone_area = calculate_zone_area(outer_radius, inner_radius)
        
        # Calculate population in this zone
        population_in_zone = zone_area * city_density
        
        # Calculate deaths
        deaths = population_in_zone * mortality_rates[zone_name]
        casualties['deaths_by_zone'][zone_name] = int(deaths)
        casualties['total_deaths'] += int(deaths)
        
        # Calculate injuries among survivors
        survivors = population_in_zone - deaths
        injuries = survivors * injury_rates[zone_name]
        casualties['injuries_by_zone'][zone_name] = int(injuries)
        casualties['total_injuries'] += int(injuries)
        
        casualties['total_affected'] += int(population_in_zone)
    
    return casualties


def format_number(num):
    """Format large numbers with appropriate suffixes."""
    if num >= 1_000_000:
        return f"{num/1_000_000:.2f} million"
    elif num >= 1_000:
        return f"{num/1_000:.2f} thousand"
    else:
        return f"{int(num)}"

