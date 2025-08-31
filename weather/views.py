from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.db.models import Q
from .models import WeatherData, WeatherForecast, WeatherAlert
from crops.models import Crop


def weather_home(request):
    """Weather home page"""
    # Get current weather for major cities
    major_cities = ['Hyderabad', 'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata']
    current_weather = {}
    
    for city in major_cities:
        weather = WeatherData.objects.filter(
            location__icontains=city,
            is_current=True
        ).first()
        if weather:
            current_weather[city] = weather
    
    # Get active weather alerts
    active_alerts = WeatherAlert.objects.filter(is_active=True)[:5]
    
    context = {
        'current_weather': current_weather,
        'active_alerts': active_alerts,
    }
    return render(request, 'weather/home.html', context)


def weather_detail(request, location):
    """Weather detail for specific location"""
    # Get current weather
    current_weather = WeatherData.objects.filter(
        location__icontains=location,
        is_current=True
    ).first()
    
    # Get 7-day forecast
    forecasts = WeatherForecast.objects.filter(
        location__icontains=location
    ).order_by('date')[:7]
    
    # Get weather alerts for location
    alerts = WeatherAlert.objects.filter(
        location__icontains=location,
        is_active=True
    )
    
    context = {
        'location': location,
        'current_weather': current_weather,
        'forecasts': forecasts,
        'alerts': alerts,
    }
    return render(request, 'weather/detail.html', context)


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
    """Weather forecast page"""
    location = request.GET.get('location', '')
    forecasts = []
    
    if location:
        forecasts = WeatherForecast.objects.filter(
            location__icontains=location
        ).order_by('date')[:7]
    
    context = {
        'location': location,
        'forecasts': forecasts,
    }
    return render(request, 'weather/forecast.html', context)


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

