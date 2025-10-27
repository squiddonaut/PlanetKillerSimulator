"""
Test Suite for Planet Killer Simulator
Tests physics calculations and core functionality
"""

import unittest
import math
from meteor_physics import MeteorMaterial, ImpactCalculator
from cities import CitiesDatabase


class TestMeteorMaterial(unittest.TestCase):
    """Test MeteorMaterial class"""
    
    def test_get_density_iron(self):
        """Test getting density for iron"""
        density = MeteorMaterial.get_density('iron')
        self.assertEqual(density, 7870)
    
    def test_get_density_stone(self):
        """Test getting density for stone"""
        density = MeteorMaterial.get_density('stone')
        self.assertEqual(density, 3300)
    
    def test_get_density_case_insensitive(self):
        """Test that material lookup is case-insensitive"""
        density1 = MeteorMaterial.get_density('IRON')
        density2 = MeteorMaterial.get_density('iron')
        self.assertEqual(density1, density2)
    
    def test_get_density_invalid_returns_default(self):
        """Test that invalid material returns default (stone)"""
        density = MeteorMaterial.get_density('invalid_material')
        self.assertEqual(density, 3300)  # Stone density
    
    def test_get_all_materials(self):
        """Test getting all materials"""
        materials = MeteorMaterial.get_all_materials()
        self.assertIn('iron', materials)
        self.assertIn('stone', materials)
        self.assertIn('ice', materials)
    
    def test_get_material_info(self):
        """Test getting material info"""
        info = MeteorMaterial.get_material_info('iron')
        self.assertEqual(info['density'], 7870)
        self.assertEqual(info['name'], 'Iron')
        self.assertIn('description', info)


class TestImpactCalculator(unittest.TestCase):
    """Test ImpactCalculator class"""
    
    def test_calculate_mass_sphere(self):
        """Test mass calculation for a spherical meteor"""
        # 10 meter diameter iron meteor
        diameter = 10  # meters
        density = 7870  # kg/m³
        
        mass = ImpactCalculator.calculate_mass(diameter, density)
        
        # Expected: Volume = (4/3) * π * r³ = (4/3) * π * 5³ = 523.6 m³
        # Mass = 523.6 * 7870 = 4,120,732 kg
        expected_volume = (4/3) * math.pi * (5 ** 3)
        expected_mass = expected_volume * density
        
        self.assertAlmostEqual(mass, expected_mass, places=2)
    
    def test_calculate_kinetic_energy(self):
        """Test kinetic energy calculation"""
        mass = 1000  # kg
        velocity = 20000  # m/s
        
        energy = ImpactCalculator.calculate_kinetic_energy(mass, velocity)
        
        # Expected: KE = 0.5 * m * v² = 0.5 * 1000 * 20000² = 2e11 J
        expected_energy = 0.5 * mass * (velocity ** 2)
        
        self.assertEqual(energy, expected_energy)
    
    def test_energy_to_tnt_kilotons(self):
        """Test conversion of energy to TNT kilotons"""
        # Hiroshima bomb was about 15 kilotons = 6.276e13 Joules
        energy = 6.276e13
        
        kt = ImpactCalculator.energy_to_tnt_kilotons(energy)
        
        self.assertAlmostEqual(kt, 15, places=0)
    
    def test_calculate_crater_diameter_positive(self):
        """Test that crater diameter is positive"""
        energy = 1e15  # 1 petajoule
        
        diameter = ImpactCalculator.calculate_crater_diameter(energy)
        
        self.assertGreater(diameter, 0)
    
    def test_calculate_destruction_radius(self):
        """Test destruction radius calculation"""
        energy = 1e15  # 1 petajoule
        
        radii = ImpactCalculator.calculate_destruction_radius(energy)
        
        # Check all expected keys exist
        self.assertIn('total_destruction', radii)
        self.assertIn('severe_damage', radii)
        self.assertIn('moderate_damage', radii)
        self.assertIn('light_damage', radii)
        self.assertIn('fireball', radii)
        
        # Check that radii increase with damage severity
        self.assertGreater(radii['light_damage'], radii['moderate_damage'])
        self.assertGreater(radii['moderate_damage'], radii['severe_damage'])
        self.assertGreater(radii['severe_damage'], radii['total_destruction'])
    
    def test_calculate_impact_effects_complete(self):
        """Test complete impact effects calculation"""
        diameter = 50  # meters
        velocity = 20000  # m/s
        material = 'iron'
        
        impact_data = ImpactCalculator.calculate_impact_effects(
            diameter, velocity, material
        )
        
        # Check all expected keys exist
        expected_keys = [
            'diameter_m', 'velocity_ms', 'material', 'density_kgm3',
            'mass_kg', 'energy_joules', 'tnt_equivalent_kt',
            'crater_diameter_m', 'destruction_zones'
        ]
        
        for key in expected_keys:
            self.assertIn(key, impact_data)
        
        # Check values are reasonable
        self.assertEqual(impact_data['diameter_m'], diameter)
        self.assertEqual(impact_data['velocity_ms'], velocity)
        self.assertEqual(impact_data['material'], material)
        self.assertGreater(impact_data['mass_kg'], 0)
        self.assertGreater(impact_data['energy_joules'], 0)
        self.assertGreater(impact_data['tnt_equivalent_kt'], 0)
    
    def test_tunguska_like_event(self):
        """Test simulation of Tunguska-like event"""
        # Tunguska was estimated at 50-60 meters, ~15km/s, stony
        diameter = 50  # meters
        velocity = 15000  # m/s
        material = 'stone'
        
        impact_data = ImpactCalculator.calculate_impact_effects(
            diameter, velocity, material
        )
        
        # Tunguska was ~10-15 megatons
        # Our calculation should be in the ballpark
        tnt_megatons = impact_data['tnt_equivalent_kt'] / 1000
        
        # Should be at least a few megatons
        self.assertGreater(tnt_megatons, 1)


class TestCitiesDatabase(unittest.TestCase):
    """Test CitiesDatabase class"""
    
    def test_get_city_exists(self):
        """Test getting a city that exists"""
        city = CitiesDatabase.get_city('New York')
        
        self.assertIsNotNone(city)
        self.assertEqual(city['country'], 'USA')
        self.assertIn('latitude', city)
        self.assertIn('longitude', city)
        self.assertIn('population', city)
    
    def test_get_city_not_exists(self):
        """Test getting a city that doesn't exist"""
        city = CitiesDatabase.get_city('Atlantis')
        
        self.assertIsNone(city)
    
    def test_get_all_cities(self):
        """Test getting all cities"""
        cities = CitiesDatabase.get_all_cities()
        
        self.assertIsInstance(cities, list)
        self.assertGreater(len(cities), 0)
        self.assertIn('New York', cities)
        self.assertIn('Tokyo', cities)
    
    def test_get_cities_by_country(self):
        """Test getting cities by country"""
        usa_cities = CitiesDatabase.get_cities_by_country('USA')
        
        self.assertIn('New York', usa_cities)
        self.assertIn('Los Angeles', usa_cities)
        self.assertNotIn('London', usa_cities)
    
    def test_search_cities(self):
        """Test searching for cities"""
        results = CitiesDatabase.search_cities('york')
        
        self.assertIn('New York', results)
    
    def test_search_cities_case_insensitive(self):
        """Test that city search is case-insensitive"""
        results1 = CitiesDatabase.search_cities('TOKYO')
        results2 = CitiesDatabase.search_cities('tokyo')
        
        self.assertEqual(results1, results2)


class TestPhysicsConsistency(unittest.TestCase):
    """Test physical consistency of calculations"""
    
    def test_larger_meteor_more_energy(self):
        """Test that larger meteors have more energy"""
        impact1 = ImpactCalculator.calculate_impact_effects(10, 20000, 'iron')
        impact2 = ImpactCalculator.calculate_impact_effects(20, 20000, 'iron')
        
        self.assertGreater(impact2['energy_joules'], impact1['energy_joules'])
    
    def test_faster_meteor_more_energy(self):
        """Test that faster meteors have more energy"""
        impact1 = ImpactCalculator.calculate_impact_effects(10, 10000, 'iron')
        impact2 = ImpactCalculator.calculate_impact_effects(10, 20000, 'iron')
        
        self.assertGreater(impact2['energy_joules'], impact1['energy_joules'])
    
    def test_denser_material_more_mass(self):
        """Test that denser materials have more mass for same size"""
        impact1 = ImpactCalculator.calculate_impact_effects(10, 20000, 'ice')
        impact2 = ImpactCalculator.calculate_impact_effects(10, 20000, 'iron')
        
        self.assertGreater(impact2['mass_kg'], impact1['mass_kg'])


if __name__ == '__main__':
    unittest.main()
