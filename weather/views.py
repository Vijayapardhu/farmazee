from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.translation import gettext as _
from django.db.models import Q
from django.utils import timezone
from .models import WeatherData, WeatherForecast, WeatherAlert
from .advanced_weather_service import advanced_weather_service
from crops.models import Crop


def weather_home(request):
    """Weather home page with advanced Open-Meteo data"""
    # Default city
    city = "hyderabad"
    
    # Get current weather using advanced service
    current_weather = advanced_weather_service.get_current_weather(city)
    
    # Get 5-day forecast
    forecast = advanced_weather_service.get_5_day_forecast(city)
    
    # Get farming recommendations
    recommendations = advanced_weather_service.get_farming_recommendations(current_weather)
    
    # Get weather alerts
    alerts = advanced_weather_service.get_weather_alerts(city)
    
    context = {
        'current_weather': current_weather,
        'forecast': forecast,
        'recommendations': recommendations,
        'alerts': alerts,
        'city': city.title(),
        'coordinates': advanced_weather_service.city_coordinates.get(city.lower(), {'lat': 17.3850, 'lon': 78.4867})
    }
    return render(request, 'weather/advanced_home.html', context)


def weather_detail(request, location):
    """Weather detail for specific location using advanced service"""
    # Convert location to lowercase for city lookup
    city = location.lower()
    
    # Get current weather using advanced service
    current_weather = advanced_weather_service.get_current_weather(city)
    
    # Get 5-day forecast
    forecasts = advanced_weather_service.get_5_day_forecast(city)
    
    # Get weather alerts
    alerts = advanced_weather_service.get_weather_alerts(city)
    
    # Get farming recommendations
    recommendations = advanced_weather_service.get_farming_recommendations(current_weather)
    
    context = {
        'location': location,
        'city': city,
        'current_weather': current_weather,
        'forecasts': forecasts,
        'alerts': alerts,
        'recommendations': recommendations,
        'coordinates': advanced_weather_service.city_coordinates.get(city, {'lat': 17.3850, 'lon': 78.4867})
    }
    return render(request, 'weather/advanced_home.html', context)


@login_required
def weather_dashboard(request):
    """Personalized weather dashboard"""
    user_profile = request.user.profile
    
    # Get weather for user's location
    weather_data = None
    forecasts = []
    alerts = []
    
    if user_profile.village:
        weather_data = WeatherData.objects.filter(
            location__icontains=user_profile.village,
            is_current=True
        ).first()
        
        forecasts = WeatherForecast.objects.filter(
            location__icontains=user_profile.village
        ).order_by('date')[:5]
        
        alerts = WeatherAlert.objects.filter(
            location__icontains=user_profile.village,
            is_active=True
        )
    
    context = {
        'weather_data': weather_data,
        'forecasts': forecasts,
        'alerts': alerts,
        'user_profile': user_profile,
    }
    return render(request, 'weather/dashboard.html', context)


def weather_alerts(request):
    """Weather alerts page"""
    alerts = WeatherAlert.objects.filter(is_active=True).order_by('-created_at')
    
    # Filter by alert type if provided
    alert_type = request.GET.get('type')
    if alert_type:
        alerts = alerts.filter(alert_type=alert_type)
    
    # Filter by severity if provided
    severity = request.GET.get('severity')
    if severity:
        alerts = alerts.filter(severity=severity)
    
    context = {
        'alerts': alerts,
        'alert_types': WeatherAlert.ALERT_TYPES,
        'severity_levels': WeatherAlert.SEVERITY_LEVELS,
    }
    return render(request, 'weather/alerts.html', context)


def weather_forecast(request):
    """Weather forecast page using advanced service"""
    city = request.GET.get('location', 'hyderabad').lower()
    
    # Get forecast data
    forecasts = advanced_weather_service.get_5_day_forecast(city)
    
    # Get current weather for comparison
    current_weather = advanced_weather_service.get_current_weather(city)
    
    context = {
        'location': city.title(),
        'city': city,
        'forecasts': forecasts,
        'current_weather': current_weather,
        'coordinates': advanced_weather_service.city_coordinates.get(city, {'lat': 17.3850, 'lon': 78.4867})
    }
    return render(request, 'weather/advanced_home.html', context)


def weather_api(request, location):
    """Weather API endpoint"""
    try:
        weather_data = WeatherData.objects.filter(
            location__icontains=location,
            is_current=True
        ).first()
        
        if weather_data:
            return JsonResponse({
                'location': weather_data.location,
                'temperature': float(weather_data.temperature),
                'humidity': weather_data.humidity,
                'description': weather_data.description,
                'wind_speed': float(weather_data.wind_speed) if weather_data.wind_speed else None,
                'pressure': float(weather_data.pressure) if weather_data.pressure else None,
            })
        else:
            return JsonResponse({'error': 'Weather data not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def forecast_api(request, location):
    """Weather forecast API endpoint"""
    try:
        forecasts = WeatherForecast.objects.filter(
            location__icontains=location
        ).order_by('date')[:7]
        
        forecast_data = []
        for forecast in forecasts:
            forecast_data.append({
                'date': forecast.date.strftime('%Y-%m-%d'),
                'min_temperature': float(forecast.min_temperature) if forecast.min_temperature else None,
                'max_temperature': float(forecast.max_temperature) if forecast.max_temperature else None,
                'humidity': forecast.humidity,
                'description': forecast.description,
                'precipitation_probability': float(forecast.precipitation_probability) if forecast.precipitation_probability else None,
            })
        
        return JsonResponse({'forecasts': forecast_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def update_weather_data(request):
    """API endpoint to update weather data for a specific city"""
    try:
        city = request.POST.get('city', 'hyderabad').lower()
        
        # Get live weather data from Open-Meteo API
        current_weather = advanced_weather_service.get_current_weather(city)
        
        if not current_weather:
            return JsonResponse({'error': 'Failed to fetch weather data'}, status=500)
        
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
                'updated_at': timezone.now(),
            }
        )
        
        # Get farming recommendations
        recommendations = advanced_weather_service.get_farming_recommendations(current_weather)
        
        return JsonResponse({
            'success': True,
            'city': city.title(),
            'weather': current_weather,
            'recommendations': recommendations,
            'updated_at': weather_data.updated_at.isoformat(),
            'created': created
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def get_live_weather_api(request):
    """API endpoint to get live weather data without caching"""
    try:
        city = request.GET.get('city', 'hyderabad').lower()
        
        # Get live weather data directly from API (bypass cache)
        current_weather = advanced_weather_service.get_current_weather(city, use_cache=False)
        
        if not current_weather:
            return JsonResponse({'error': 'Failed to fetch live weather data'}, status=500)
        
        # Get farming recommendations
        recommendations = advanced_weather_service.get_farming_recommendations(current_weather)
        
        return JsonResponse({
            'success': True,
            'city': city.title(),
            'weather': current_weather,
            'recommendations': recommendations,
            'timestamp': timezone.now().isoformat(),
            'source': 'live_api'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

