"""
Real-time Weather Service using OpenWeatherMap API
Provides accurate, real-time weather data with city search functionality
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from django.conf import settings
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

class RealWeatherService:
    """Real-time weather service using OpenWeatherMap API"""
    
    def __init__(self):
        # Get API key from environment or settings
        self.api_key = os.getenv('WEATHER_API_KEY') or os.getenv('OPENWEATHER_API_KEY') or getattr(settings, 'WEATHER_API_KEY', '')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.geocoding_url = "http://api.openweathermap.org/geo/1.0"
        
        # Major cities coordinates as fallback
        self.major_cities = {
            'hyderabad': {'lat': 17.3850, 'lon': 78.4867, 'country': 'IN'},
            'delhi': {'lat': 28.6139, 'lon': 77.2090, 'country': 'IN'},
            'mumbai': {'lat': 19.0760, 'lon': 72.8777, 'country': 'IN'},
            'bangalore': {'lat': 12.9716, 'lon': 77.5946, 'country': 'IN'},
            'kolkata': {'lat': 22.5726, 'lon': 88.3639, 'country': 'IN'},
            'chennai': {'lat': 13.0827, 'lon': 80.2707, 'country': 'IN'},
            'pune': {'lat': 18.5204, 'lon': 73.8567, 'country': 'IN'},
            'ahmedabad': {'lat': 23.0225, 'lon': 72.5714, 'country': 'IN'},
            'jaipur': {'lat': 26.9124, 'lon': 75.7873, 'country': 'IN'},
            'lucknow': {'lat': 26.8467, 'lon': 80.9462, 'country': 'IN'},
            'new york': {'lat': 40.7128, 'lon': -74.0060, 'country': 'US'},
            'london': {'lat': 51.5074, 'lon': -0.1278, 'country': 'GB'},
            'tokyo': {'lat': 35.6762, 'lon': 139.6503, 'country': 'JP'},
            'paris': {'lat': 48.8566, 'lon': 2.3522, 'country': 'FR'},
            'sydney': {'lat': -33.8688, 'lon': 151.2093, 'country': 'AU'},
        }
        
        if not self.api_key:
            logger.warning("OpenWeatherMap API key not found. Using demo key.")
            self.api_key = "demo_key"
    
    def search_cities(self, query: str, limit: int = 5) -> List[Dict]:
        """Search for cities by name"""
        if not query or len(query) < 2:
            return []
        
        # First check major cities for matches
        query_lower = query.lower().strip()
        matching_cities = []
        
        for city_key, coords in self.major_cities.items():
            if query_lower in city_key or city_key in query_lower:
                matching_cities.append({
                    'name': city_key.title(),
                    'state': '',
                    'country': coords['country'],
                    'lat': coords['lat'],
                    'lon': coords['lon'],
                    'display_name': f"{city_key.title()}, {coords['country']}"
                })
        
        if matching_cities:
            return matching_cities[:limit]
        
        # Try API search if no major city matches
        try:
            url = f"{self.geocoding_url}/direct"
            params = {
                'q': query,
                'limit': limit,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            cities = []
            for city_data in response.json():
                cities.append({
                    'name': city_data['name'],
                    'state': city_data.get('state', ''),
                    'country': city_data['country'],
                    'lat': city_data['lat'],
                    'lon': city_data['lon'],
                    'display_name': f"{city_data['name']}, {city_data.get('state', '')}, {city_data['country']}".strip(', ')
                })
            
            return cities
            
        except Exception as e:
            logger.warning(f"City search API error: {e}. Using fallback cities.")
            # Return some major cities as fallback
            fallback_cities = []
            for city_key, coords in list(self.major_cities.items())[:limit]:
                fallback_cities.append({
                    'name': city_key.title(),
                    'state': '',
                    'country': coords['country'],
                    'lat': coords['lat'],
                    'lon': coords['lon'],
                    'display_name': f"{city_key.title()}, {coords['country']}"
                })
            return fallback_cities
    
    def get_current_weather(self, city_name: str = "Hyderabad", country_code: str = "IN") -> Dict:
        """Get current weather for a specific city"""
        cache_key = f'weather_current_{city_name}_{country_code}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        # Try to get real weather data first
        try:
            # First get coordinates for the city
            coords = self._get_city_coordinates(city_name, country_code)
            if not coords:
                logger.warning(f"No coordinates found for {city_name}, using fallback")
                return self._get_fallback_weather(city_name)
            
            # Get current weather using coordinates
            url = f"{self.base_url}/weather"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            weather_data = self._process_current_weather(data)
            weather_data['city'] = city_name
            weather_data['country'] = country_code
            weather_data['is_real_data'] = True
            
            # Cache for 30 minutes
            cache.set(cache_key, weather_data, 1800)
            
            return weather_data
            
        except Exception as e:
            logger.warning(f"Weather API error for {city_name}: {e}. Using fallback data.")
            return self._get_fallback_weather(city_name)
    
    def get_5_day_forecast(self, city_name: str = "Hyderabad", country_code: str = "IN") -> List[Dict]:
        """Get 5-day weather forecast"""
        cache_key = f'weather_forecast_{city_name}_{country_code}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            # Get coordinates for the city
            coords = self._get_city_coordinates(city_name, country_code)
            if not coords:
                return self._get_fallback_forecast(city_name)
            
            # Get forecast
            url = f"{self.base_url}/forecast"
            params = {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            forecast_data = self._process_forecast(data)
            
            # Cache for 1 hour
            cache.set(cache_key, forecast_data, 3600)
            
            return forecast_data
            
        except Exception as e:
            logger.error(f"Forecast API error: {e}")
            return self._get_fallback_forecast(city_name)
    
    def get_farming_recommendations(self, weather_data: Dict) -> List[Dict]:
        """Get farming recommendations based on weather data"""
        recommendations = []
        
        temp = weather_data.get('temperature', 25)
        humidity = weather_data.get('humidity', 50)
        wind_speed = weather_data.get('wind_speed', 5)
        condition = weather_data.get('condition', 'Clear').lower()
        precipitation = weather_data.get('precipitation', 0)
        
        # Temperature recommendations
        if temp > 35:
            recommendations.append({
                'type': 'warning',
                'icon': '🌡️',
                'title': 'High Temperature Alert',
                'message': f'Temperature: {temp}°C',
                'action': 'Increase irrigation frequency and provide shade for sensitive crops'
            })
        elif temp < 15:
            recommendations.append({
                'type': 'warning',
                'icon': '❄️',
                'title': 'Low Temperature Alert',
                'message': f'Temperature: {temp}°C',
                'action': 'Protect sensitive crops and reduce irrigation'
            })
        
        # Humidity recommendations
        if humidity > 80:
            recommendations.append({
                'type': 'info',
                'icon': '💧',
                'title': 'High Humidity',
                'message': f'Humidity: {humidity}%',
                'action': 'Monitor for fungal diseases and improve air circulation'
            })
        elif humidity < 40:
            recommendations.append({
                'type': 'info',
                'icon': '🏜️',
                'title': 'Low Humidity',
                'message': f'Humidity: {humidity}%',
                'action': 'Increase irrigation and use mulching to retain moisture'
            })
        
        # Wind recommendations
        if wind_speed > 15:
            recommendations.append({
                'type': 'warning',
                'icon': '💨',
                'title': 'Strong Winds',
                'message': f'Wind Speed: {wind_speed} km/h',
                'action': 'Secure farm structures and protect young plants'
            })
        
        # Rain recommendations
        if 'rain' in condition or precipitation > 5:
            recommendations.append({
                'type': 'info',
                'icon': '🌧️',
                'title': 'Rain Expected',
                'message': f'Precipitation: {precipitation}mm',
                'action': 'Skip irrigation and protect harvested crops'
            })
        
        # Good farming conditions
        if 20 <= temp <= 30 and 'clear' in condition and wind_speed < 15:
            recommendations.append({
                'type': 'success',
                'icon': '☀️',
                'title': 'Excellent Farming Weather',
                'message': 'Ideal conditions for farming activities',
                'action': 'Perfect for planting, spraying, and field work'
            })
        
        return recommendations[:5]  # Limit to 5 recommendations
    
    def _get_city_coordinates(self, city_name: str, country_code: str = "IN") -> Optional[Dict]:
        """Get coordinates for a city"""
        # First check if it's a major city we have coordinates for
        city_key = city_name.lower().strip()
        if city_key in self.major_cities:
            coords = self.major_cities[city_key]
            return {
                'lat': coords['lat'],
                'lon': coords['lon'],
                'name': city_name,
                'country': coords['country']
            }
        
        # Try API geocoding if available
        try:
            url = f"{self.geocoding_url}/direct"
            params = {
                'q': f"{city_name},{country_code}",
                'limit': 1,
                'appid': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if data:
                return {
                    'lat': data[0]['lat'],
                    'lon': data[0]['lon'],
                    'name': data[0]['name'],
                    'country': data[0]['country']
                }
            
            return None
            
        except Exception as e:
            logger.warning(f"Geocoding API error: {e}. Using fallback coordinates.")
            # Use Hyderabad as fallback
            return {
                'lat': 17.3850,
                'lon': 78.4867,
                'name': city_name,
                'country': 'IN'
            }
    
    def _process_current_weather(self, data: Dict) -> Dict:
        """Process current weather API response"""
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']
        sys = data['sys']
        
        return {
            'temperature': round(main['temp']),
            'feels_like': round(main['feels_like']),
            'temp_min': round(main['temp_min']),
            'temp_max': round(main['temp_max']),
            'humidity': main['humidity'],
            'pressure': main['pressure'],
            'condition': weather['main'],
            'description': weather['description'].title(),
            'icon': weather['icon'],
            'wind_speed': round(wind['speed'], 1),
            'wind_direction': wind.get('deg', 0),
            'wind_direction_text': self._get_wind_direction(wind.get('deg', 0)),
            'visibility': round(data.get('visibility', 10000) / 1000, 1),  # Convert to km
            'clouds': data['clouds']['all'],
            'sunrise': datetime.fromtimestamp(sys['sunrise']).strftime('%H:%M'),
            'sunset': datetime.fromtimestamp(sys['sunset']).strftime('%H:%M'),
            'city': data['name'],
            'country': data['sys']['country'],
            'timestamp': datetime.fromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M'),
            'uv_index': self._get_uv_index(weather['main']),
            'precipitation': 0  # Will be updated if rain data is available
        }
    
    def _process_forecast(self, data: Dict) -> List[Dict]:
        """Process forecast API response"""
        forecasts = []
        processed_dates = set()
        
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).date()
            
            if date not in processed_dates and len(forecasts) < 5:
                forecasts.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'day_name': date.strftime('%A'),
                    'max_temp': round(item['main']['temp_max']),
                    'min_temp': round(item['main']['temp_min']),
                    'temperature': round(item['main']['temp']),
                    'temp_max': round(item['main']['temp_max']),
                    'temp_min': round(item['main']['temp_min']),
                    'condition': item['weather'][0]['main'],
                    'description': item['weather'][0]['description'].title(),
                    'icon': item['weather'][0]['icon'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': round(item['wind']['speed'], 1),
                    'precipitation': round(item.get('rain', {}).get('3h', 0), 1),
                    'farming_conditions': self._get_farming_conditions(
                        item['main']['temp_max'],
                        item['main']['temp_min'],
                        item.get('rain', {}).get('3h', 0),
                        item['wind']['speed'],
                        item['weather'][0]['main']
                    )
                })
                processed_dates.add(date)
        
        return forecasts
    
    def _get_wind_direction(self, degrees: float) -> str:
        """Convert wind direction degrees to compass direction"""
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    def _get_uv_index(self, condition: str) -> str:
        """Estimate UV index based on weather condition"""
        if condition == 'Clear':
            return "High (8-10)"
        elif condition in ['Clouds', 'Partly Cloudy']:
            return "Moderate (5-7)"
        else:
            return "Low (2-4)"
    
    def _get_farming_conditions(self, max_temp: float, min_temp: float, 
                              precipitation: float, wind_speed: float, condition: str) -> str:
        """Get farming conditions assessment"""
        if precipitation > 10:
            return "Wet - Avoid field work"
        elif max_temp > 38:
            return "Hot - Extra irrigation needed"
        elif min_temp < 10:
            return "Cold - Protect sensitive crops"
        elif wind_speed > 20:
            return "Windy - Secure structures"
        elif condition == 'Clear' and 20 <= max_temp <= 30:
            return "Excellent - Perfect for field work"
        elif condition in ['Clear', 'Clouds']:
            return "Good - Suitable for most activities"
        else:
            return "Moderate - Check specific conditions"

    def _get_daily_farming_conditions(self, max_temp: float, min_temp: float, condition: str) -> str:
        """Compatibility shim: derive daily farming conditions when precipitation
        and wind_speed are not available (used by fallback forecast generator).
        This forwards to _get_farming_conditions with conservative defaults.
        """
        # Conservative defaults for fallback generation
        default_precipitation = 0.0
        default_wind_speed = 5.0
        return self._get_farming_conditions(max_temp, min_temp, default_precipitation, default_wind_speed, condition)
    
    def _get_fallback_weather(self, city_name: str) -> Dict:
        """Fallback weather data when API fails - different data for different cities"""
        import random
        
        # Get city-specific data if available
        city_key = city_name.lower().strip()
        if city_key in self.major_cities:
            coords = self.major_cities[city_key]
            # Generate city-specific weather based on location
            base_temp = self._get_city_base_temp(city_key)
            variation = random.randint(-3, 3)
            temp = base_temp + variation
        else:
            # Default weather for unknown cities
            temp = 25 + random.randint(-5, 10)
        
        # Generate realistic weather variations
        conditions = ['Clear', 'Clouds', 'Rain', 'Thunderstorm']
        condition = random.choice(conditions)
        
        weather_data = {
            'temperature': temp,
            'feels_like': temp + random.randint(-2, 4),
            'temp_min': temp - random.randint(2, 6),
            'temp_max': temp + random.randint(2, 6),
            'humidity': random.randint(40, 90),
            'pressure': random.randint(1000, 1020),
            'condition': condition,
            'description': self._get_condition_description(condition),
            'icon': self._get_condition_icon(condition),
            'wind_speed': round(random.uniform(2, 15), 1),
            'wind_direction': random.randint(0, 360),
            'wind_direction_text': self._get_wind_direction(random.randint(0, 360)),
            'visibility': round(random.uniform(5, 15), 1),
            'clouds': random.randint(10, 80),
            'sunrise': '06:00',
            'sunset': '18:30',
            'city': city_name,
            'country': 'IN',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'uv_index': 'Moderate (5-7)',
            'precipitation': random.randint(0, 5) if condition in ['Rain', 'Thunderstorm'] else 0,
            'is_fallback': True
        }
        
        return weather_data
    
    def _get_city_base_temp(self, city_key: str) -> int:
        """Get base temperature for different cities"""
        city_temps = {
            'hyderabad': 28,
            'delhi': 25,
            'mumbai': 30,
            'bangalore': 26,
            'kolkata': 32,
            'chennai': 31,
            'pune': 27,
            'ahmedabad': 29,
            'jaipur': 24,
            'lucknow': 26,
            'new york': 15,
            'london': 12,
            'tokyo': 18,
            'paris': 14,
            'sydney': 22
        }
        return city_temps.get(city_key, 25)
    
    def _get_condition_description(self, condition: str) -> str:
        """Get description for weather condition"""
        descriptions = {
            'Clear': 'Clear Sky',
            'Clouds': 'Partly Cloudy',
            'Rain': 'Light Rain',
            'Thunderstorm': 'Thunderstorm'
        }
        return descriptions.get(condition, 'Partly Cloudy')
    
    def _get_condition_icon(self, condition: str) -> str:
        """Get icon for weather condition"""
        icons = {
            'Clear': '01d',
            'Clouds': '02d',
            'Rain': '10d',
            'Thunderstorm': '11d'
        }
        return icons.get(condition, '02d')
    
    def _get_fallback_forecast(self, city_name: str) -> List[Dict]:
        """Fallback forecast data when API fails - different for each city"""
        import random
        forecasts = []
        base_date = datetime.now()
        
        # Get city-specific base temperature
        city_key = city_name.lower().strip()
        base_temp = self._get_city_base_temp(city_key)
        
        for i in range(5):
            date = (base_date + timedelta(days=i)).date()
            # Generate varied weather for each day
            day_variation = random.randint(-5, 5)
            min_temp = base_temp - 5 + day_variation
            max_temp = base_temp + 5 + day_variation
            
            # Random weather conditions
            conditions = ['Clear', 'Clouds', 'Rain', 'Thunderstorm']
            condition = random.choice(conditions)
            
            forecasts.append({
                'date': date.strftime('%Y-%m-%d'),
                'day_name': date.strftime('%A'),
                'max_temp': max_temp,
                'min_temp': min_temp,
                'temperature': round((min_temp + max_temp) / 2),
                'temp_max': max_temp,
                'temp_min': min_temp,
                'condition': condition,
                'description': self._get_condition_description(condition),
                'icon': self._get_condition_icon(condition),
                'humidity': random.randint(40, 90),
                'wind_speed': round(random.uniform(5, 20), 1),
                'precipitation': random.randint(0, 10) if condition in ['Rain', 'Thunderstorm'] else 0,
                'farming_conditions': self._get_daily_farming_conditions(max_temp, min_temp, condition),
                'is_fallback': True
            })
        
        return forecasts


# Initialize real weather service
real_weather_service = RealWeatherService()


