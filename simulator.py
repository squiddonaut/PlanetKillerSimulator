#!/usr/bin/env python3
"""
Planet Killer Simulator - Main CLI Interface
A meteor impact simulator for visualizing destruction on Earth
"""

import sys
from meteor_physics import MeteorMaterial, ImpactCalculator
from cities import CitiesDatabase
from visualization import ImpactVisualizer


def print_banner():
    """Print application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════╗
║                  PLANET KILLER SIMULATOR                         ║
║              Meteor Impact Analysis System                       ║
╚══════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def get_float_input(prompt, min_val=None, max_val=None):
    """Get and validate float input from user"""
    while True:
        try:
            value = float(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}")
                continue
            if max_val is not None and value > max_val:
                print(f"Value must be at most {max_val}")
                continue
            return value
        except ValueError:
            print("Please enter a valid number")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit(0)


def get_choice_input(prompt, valid_choices):
    """Get and validate choice input from user"""
    while True:
        try:
            choice = input(prompt).strip()
            if choice.lower() in [c.lower() for c in valid_choices]:
                # Return the choice matching case from valid_choices
                for valid in valid_choices:
                    if valid.lower() == choice.lower():
                        return valid
            print(f"Please choose from: {', '.join(valid_choices)}")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit(0)


def select_city():
    """Allow user to select a city"""
    cities = CitiesDatabase.get_all_cities()
    cities_sorted = sorted(cities)
    
    print("\n" + "="*70)
    print("AVAILABLE CITIES:")
    print("="*70)
    
    for i, city in enumerate(cities_sorted, 1):
        city_info = CitiesDatabase.get_city(city)
        print(f"{i:2d}. {city:20s} ({city_info['country']})")
    
    print("="*70)
    
    while True:
        try:
            choice = input("\nEnter city number or name: ").strip()
            
            # Try as number first
            try:
                index = int(choice) - 1
                if 0 <= index < len(cities_sorted):
                    return cities_sorted[index]
            except ValueError:
                pass
            
            # Try as city name
            for city in cities_sorted:
                if city.lower() == choice.lower():
                    return city
            
            print("Invalid selection. Please try again.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit(0)


def select_material():
    """Allow user to select meteor material"""
    materials = MeteorMaterial.get_all_materials()
    materials_sorted = sorted(materials)
    
    print("\n" + "="*70)
    print("AVAILABLE MATERIALS:")
    print("="*70)
    
    for i, material in enumerate(materials_sorted, 1):
        mat_info = MeteorMaterial.get_material_info(material)
        print(f"{i}. {mat_info['name']:15s} - Density: {mat_info['density']:,} kg/m³")
        print(f"   {mat_info['description']}")
    
    print("="*70)
    
    while True:
        try:
            choice = input("\nEnter material number or name: ").strip()
            
            # Try as number first
            try:
                index = int(choice) - 1
                if 0 <= index < len(materials_sorted):
                    return materials_sorted[index]
            except ValueError:
                pass
            
            # Try as material name
            for material in materials_sorted:
                if material.lower() == choice.lower():
                    return material
            
            print("Invalid selection. Please try again.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            sys.exit(0)


def run_simulation():
    """Run the meteor impact simulation"""
    print_banner()
    
    print("\nWelcome to the Planet Killer Simulator!")
    print("This program simulates meteor impacts on major Earth cities.\n")
    
    # Get meteor parameters
    print("\n" + "="*70)
    print("METEOR PARAMETERS")
    print("="*70)
    
    diameter = get_float_input(
        "\nEnter meteor diameter in meters (e.g., 10-1000): ",
        min_val=0.1
    )
    
    velocity = get_float_input(
        "Enter impact velocity in m/s (typical: 11,000-72,000): ",
        min_val=100
    )
    
    material = select_material()
    
    # Select target city
    city_name = select_city()
    city_info = CitiesDatabase.get_city(city_name)
    
    # Calculate impact effects
    print("\n" + "="*70)
    print("CALCULATING IMPACT EFFECTS...")
    print("="*70)
    
    impact_data = ImpactCalculator.calculate_impact_effects(
        diameter, velocity, material
    )
    
    # Display results
    print(ImpactVisualizer.format_impact_summary(impact_data))
    print(ImpactVisualizer.format_comparison(impact_data))
    
    # Display visualization
    print("\n" + "="*70)
    print("IMPACT VISUALIZATION")
    print("="*70)
    visualization = ImpactVisualizer.create_impact_map(
        city_name, city_info, impact_data['destruction_zones']
    )
    print(visualization)
    
    # Ask if user wants to run another simulation
    print("\n" + "="*70)
    while True:
        try:
            again = input("\nRun another simulation? (y/n): ").strip().lower()
            if again == 'y' or again == 'yes':
                print("\n\n")
                run_simulation()
                break
            elif again == 'n' or again == 'no':
                print("\nThank you for using Planet Killer Simulator!")
                print("Remember: This is a simulation. Please don't try this at home. 🌍\n")
                break
            else:
                print("Please enter 'y' or 'n'")
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting...")
            break


def main():
    """Main entry point"""
    try:
        run_simulation()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSimulation terminated by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
