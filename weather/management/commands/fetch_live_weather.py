"""
Management command to fetch live weather data from Open-Meteo API
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from weather.advanced_weather_service import advanced_weather_service
from weather.models import WeatherData, WeatherForecast
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch live weather data from Open-Meteo API and update database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cities',
            nargs='+',
            help='Specific cities to fetch weather for',
            default=['hyderabad', 'delhi', 'mumbai', 'bangalore', 'chennai']
        )
        parser.add_argument(
            '--forecast',
            action='store_true',
            help='Also fetch 5-day forecast data',
        )

    def handle(self, *args, **options):
        self.stdout.write('Fetching live weather data...')
        
        cities = options['cities']
        fetch_forecast = options['forecast']
        
        success_count = 0
        error_count = 0
        
        for city in cities:
            try:
                self.stdout.write(f'Fetching weather for {city.title()}...')
                
                # Get current weather
                current_weather = advanced_weather_service.get_current_weather(city)
                
                if current_weather:
                    # Update or create WeatherData record
                    weather_data, created = WeatherData.objects.update_or_create(
                        location=city.title(),
                        defaults={
                            'latitude': current_weather.get('latitude'),
                            'longitude': current_weather.get('longitude'),
                            'temperature': current_weather.get('temperature'),
                            'humidity': current_weather.get('humidity'),
                            'wind_speed': current_weather.get('wind_speed'),
                            'wind_direction': current_weather.get('wind_direction'),
                            'pressure': current_weather.get('pressure'),
                            'description': current_weather.get('description'),
                            'icon': current_weather.get('icon'),
                            'visibility': current_weather.get('visibility', 10.0),
                            'uv_index': current_weather.get('uv_index'),
                            'is_current': True,
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'  ✓ Created new weather record for {city.title()}')
                    else:
                        self.stdout.write(f'  ✓ Updated weather record for {city.title()}')
                    
                    success_count += 1
                    
                    # Fetch forecast if requested
                    if fetch_forecast:
                        self.stdout.write(f'  Fetching 5-day forecast for {city.title()}...')
                        forecast_data = advanced_weather_service.get_5_day_forecast(city)
                        
                        if forecast_data:
                            # Clear existing forecasts for this city
                            WeatherForecast.objects.filter(location=city.title()).delete()
                            
                            # Create new forecast records
                            for day_data in forecast_data:
                                WeatherForecast.objects.create(
                                    location=city.title(),
                                    date=day_data['date'],
                                    min_temperature=day_data['min_temperature'],
                                    max_temperature=day_data['max_temperature'],
                                    humidity=day_data['humidity'],
                                    wind_speed=day_data['wind_speed'],
                                    wind_direction=day_data.get('wind_direction'),
                                    description=day_data['description'],
                                    icon=day_data.get('icon'),
                                    precipitation_probability=day_data.get('precipitation_probability'),
                                )
                            
                            self.stdout.write(f'  ✓ Updated 5-day forecast for {city.title()}')
                else:
                    self.stdout.write(f'  ✗ Failed to fetch weather for {city.title()}')
                    error_count += 1
                    
            except Exception as e:
                self.stdout.write(f'  ✗ Error fetching weather for {city.title()}: {str(e)}')
                logger.error(f'Error fetching weather for {city}: {str(e)}')
                error_count += 1
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Weather data fetch completed!')
        self.stdout.write(f'✓ Successfully updated: {success_count} cities')
        if error_count > 0:
            self.stdout.write(f'✗ Failed to update: {error_count} cities')
        
        if fetch_forecast:
            self.stdout.write(f'✓ 5-day forecasts updated for all cities')
        
        self.stdout.write('='*50)

