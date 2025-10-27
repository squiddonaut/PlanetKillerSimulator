"""
Cities Database
Contains major world cities with their coordinates and population data
"""


class CitiesDatabase:
    """Database of major world cities"""
    
    CITIES = {
        'New York': {
            'country': 'USA',
            'latitude': 40.7128,
            'longitude': -74.0060,
            'population': 8336817,
            'metro_population': 20140470
        },
        'Los Angeles': {
            'country': 'USA',
            'latitude': 34.0522,
            'longitude': -118.2437,
            'population': 3979576,
            'metro_population': 13200998
        },
        'London': {
            'country': 'UK',
            'latitude': 51.5074,
            'longitude': -0.1278,
            'population': 9002488,
            'metro_population': 14257962
        },
        'Paris': {
            'country': 'France',
            'latitude': 48.8566,
            'longitude': 2.3522,
            'population': 2165423,
            'metro_population': 12405426
        },
        'Tokyo': {
            'country': 'Japan',
            'latitude': 35.6762,
            'longitude': 139.6503,
            'population': 13960000,
            'metro_population': 37400068
        },
        'Beijing': {
            'country': 'China',
            'latitude': 39.9042,
            'longitude': 116.4074,
            'population': 21540000,
            'metro_population': 24900000
        },
        'Moscow': {
            'country': 'Russia',
            'latitude': 55.7558,
            'longitude': 37.6173,
            'population': 12500123,
            'metro_population': 17125000
        },
        'Mumbai': {
            'country': 'India',
            'latitude': 19.0760,
            'longitude': 72.8777,
            'population': 12442373,
            'metro_population': 20961472
        },
        'São Paulo': {
            'country': 'Brazil',
            'latitude': -23.5505,
            'longitude': -46.6333,
            'population': 12325232,
            'metro_population': 21846507
        },
        'Cairo': {
            'country': 'Egypt',
            'latitude': 30.0444,
            'longitude': 31.2357,
            'population': 9500000,
            'metro_population': 20900604
        },
        'Mexico City': {
            'country': 'Mexico',
            'latitude': 19.4326,
            'longitude': -99.1332,
            'population': 9209944,
            'metro_population': 21804515
        },
        'Sydney': {
            'country': 'Australia',
            'latitude': -33.8688,
            'longitude': 151.2093,
            'population': 5312163,
            'metro_population': 5312163
        },
        'Singapore': {
            'country': 'Singapore',
            'latitude': 1.3521,
            'longitude': 103.8198,
            'population': 5685807,
            'metro_population': 5685807
        },
        'Dubai': {
            'country': 'UAE',
            'latitude': 25.2048,
            'longitude': 55.2708,
            'population': 3331420,
            'metro_population': 3331420
        },
        'Berlin': {
            'country': 'Germany',
            'latitude': 52.5200,
            'longitude': 13.4050,
            'population': 3769495,
            'metro_population': 6120000
        },
        'Toronto': {
            'country': 'Canada',
            'latitude': 43.6532,
            'longitude': -79.3832,
            'population': 2930000,
            'metro_population': 6417516
        },
        'Hong Kong': {
            'country': 'China',
            'latitude': 22.3193,
            'longitude': 114.1694,
            'population': 7496981,
            'metro_population': 7496981
        },
        'Seoul': {
            'country': 'South Korea',
            'latitude': 37.5665,
            'longitude': 126.9780,
            'population': 9776000,
            'metro_population': 25514000
        },
        'Istanbul': {
            'country': 'Turkey',
            'latitude': 41.0082,
            'longitude': 28.9784,
            'population': 15462452,
            'metro_population': 15462452
        },
        'Buenos Aires': {
            'country': 'Argentina',
            'latitude': -34.6037,
            'longitude': -58.3816,
            'population': 3075646,
            'metro_population': 15153729
        }
    }
    
    @classmethod
    def get_city(cls, city_name):
        """Get information about a specific city"""
        return cls.CITIES.get(city_name)
    
    @classmethod
    def get_all_cities(cls):
        """Get list of all available cities"""
        return list(cls.CITIES.keys())
    
    @classmethod
    def get_cities_by_country(cls, country):
        """Get all cities in a specific country"""
        return {
            name: info for name, info in cls.CITIES.items()
            if info['country'] == country
        }
    
    @classmethod
    def search_cities(cls, search_term):
        """Search for cities by name (case-insensitive partial match)"""
        search_lower = search_term.lower()
        return {
            name: info for name, info in cls.CITIES.items()
            if search_lower in name.lower()
        }
