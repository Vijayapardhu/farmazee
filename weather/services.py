import requests
import json
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from .models import WeatherData, WeatherForecast, WeatherAlert


class WeatherService:
    """Weather service for API integration"""
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, location):
        """Get current weather for a location"""
        if not self.api_key:
            return self._get_mock_weather_data(location)
        
        try:
            url = f"{self.base_url}/weather"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_current_weather(data, location)
            
        except requests.RequestException as e:
            print(f"Weather API error: {e}")
            return self._get_mock_weather_data(location)
    
    def get_forecast(self, location):
        """Get weather forecast for a location"""
        if not self.api_key:
            return self._get_mock_forecast_data(location)
        
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': location,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return self._parse_forecast_data(data, location)
            
        except requests.RequestException as e:
            print(f"Weather forecast API error: {e}")
            return self._get_mock_forecast_data(location)
    
    def _parse_current_weather(self, data, location):
        """Parse current weather data from API response"""
        try:
            weather_data = {
                'location': location,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': self._get_wind_direction(data['wind'].get('deg', 0)),
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'recorded_at': timezone.now(),
            }
            
            # Save to database
            self._save_weather_data(weather_data)
            
            return weather_data
            
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
            return self._get_mock_weather_data(location)
    
    def _parse_forecast_data(self, data, location):
        """Parse forecast data from API response"""
        try:
            forecasts = []
            daily_data = {}
            
            for item in data['list']:
                date = datetime.fromtimestamp(item['dt']).date()
                
                if date not in daily_data:
                    daily_data[date] = {
                        'min_temp': float('inf'),
                        'max_temp': float('-inf'),
                        'humidity': [],
                        'wind_speed': [],
                        'descriptions': set(),
                    }
                
                daily_data[date]['min_temp'] = min(daily_data[date]['min_temp'], item['main']['temp'])
                daily_data[date]['max_temp'] = max(daily_data[date]['max_temp'], item['main']['temp'])
                daily_data[date]['humidity'].append(item['main']['humidity'])
                daily_data[date]['wind_speed'].append(item['wind']['speed'])
                daily_data[date]['descriptions'].add(item['weather'][0]['description'])
            
            for date, day_data in daily_data.items():
                if date > timezone.now().date():
                    forecast = {
                        'location': location,
                        'date': date,
                        'min_temperature': day_data['min_temp'],
                        'max_temperature': day_data['max_temp'],
                        'humidity': sum(day_data['humidity']) // len(day_data['humidity']),
                        'wind_speed': sum(day_data['wind_speed']) / len(day_data['wind_speed']),
                        'description': ', '.join(day_data['descriptions']),
                        'precipitation_probability': 0,  # API doesn't provide this in free tier
                    }
                    
                    forecasts.append(forecast)
                    self._save_forecast_data(forecast)
            
            return forecasts
            
        except KeyError as e:
            print(f"Error parsing forecast data: {e}")
            return self._get_mock_forecast_data(location)
    
    def _get_wind_direction(self, degrees):
        """Convert wind degrees to direction"""
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    def _save_weather_data(self, weather_data):
        """Save weather data to database"""
        try:
            # Mark existing current weather as not current
            WeatherData.objects.filter(
                location__icontains=weather_data['location'],
                is_current=True
            ).update(is_current=False)
            
            # Create new weather data
            WeatherData.objects.create(
                location=weather_data['location'],
                temperature=weather_data['temperature'],
                humidity=weather_data['humidity'],
                pressure=weather_data['pressure'],
                description=weather_data['description'],
                icon=weather_data['icon'],
                wind_speed=weather_data['wind_speed'],
                wind_direction=weather_data['wind_direction'],
                visibility=weather_data['visibility'],
                is_current=True
            )
        except Exception as e:
            print(f"Error saving weather data: {e}")
    
    def _save_forecast_data(self, forecast_data):
        """Save forecast data to database"""
        try:
            WeatherForecast.objects.update_or_create(
                location=forecast_data['location'],
                date=forecast_data['date'],
                defaults={
                    'min_temperature': forecast_data['min_temperature'],
                    'max_temperature': forecast_data['max_temperature'],
                    'humidity': forecast_data['humidity'],
                    'wind_speed': forecast_data['wind_speed'],
                    'description': forecast_data['description'],
                    'precipitation_probability': forecast_data['precipitation_probability'],
                }
            )
        except Exception as e:
            print(f"Error saving forecast data: {e}")
    
    def _get_mock_weather_data(self, location):
        """Get mock weather data for testing"""
        return {
            'location': location,
            'temperature': 25.0,
            'humidity': 65,
            'pressure': 1013.25,
            'description': 'Partly cloudy',
            'icon': '02d',
            'wind_speed': 5.2,
            'wind_direction': 'NE',
            'visibility': 10.0,
            'recorded_at': timezone.now(),
        }
    
    def _get_mock_forecast_data(self, location):
        """Get mock forecast data for testing"""
        forecasts = []
        for i in range(1, 8):
            date = timezone.now().date() + timedelta(days=i)
            forecasts.append({
                'location': location,
                'date': date,
                'min_temperature': 20.0 + i,
                'max_temperature': 30.0 + i,
                'humidity': 60 + (i % 20),
                'wind_speed': 3.0 + (i % 5),
                'description': 'Sunny',
                'precipitation_probability': 10 + (i % 30),
            })
        return forecasts



