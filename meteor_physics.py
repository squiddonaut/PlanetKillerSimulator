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
