"""
Advanced Weather Services for Farmazee using Open-Meteo API
Provides accurate, real-time weather data with comprehensive farming recommendations
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from django.conf import settings
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

class AdvancedWeatherService:
    """Advanced weather service using Open-Meteo API for precise farming weather data"""
    
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        # Major Indian agricultural cities with coordinates
        self.city_coordinates = {
            'hyderabad': {'lat': 17.3850, 'lon': 78.4867},
            'delhi': {'lat': 28.6139, 'lon': 77.2090},
            'mumbai': {'lat': 19.0760, 'lon': 72.8777},
            'bangalore': {'lat': 12.9716, 'lon': 77.5946},
            'kolkata': {'lat': 22.5726, 'lon': 88.3639},
            'chennai': {'lat': 13.0827, 'lon': 80.2707},
            'ahmedabad': {'lat': 23.0225, 'lon': 72.5714},
            'pune': {'lat': 18.5204, 'lon': 73.8567},
            'jaipur': {'lat': 26.9124, 'lon': 75.7873},
            'lucknow': {'lat': 26.8467, 'lon': 80.9462},
            'kanpur': {'lat': 26.4499, 'lon': 80.3319},
            'nagpur': {'lat': 21.1458, 'lon': 79.0882},
            'indore': {'lat': 22.7196, 'lon': 75.8577},
            'bhopal': {'lat': 23.2599, 'lon': 77.4126},
            'visakhapatnam': {'lat': 17.6868, 'lon': 83.2185},
            'patna': {'lat': 25.5941, 'lon': 85.1376},
            'vadodara': {'lat': 22.3072, 'lon': 73.1812},
            'ludhiana': {'lat': 30.9010, 'lon': 75.8573},
            'agra': {'lat': 27.1767, 'lon': 78.0081},
            'nashik': {'lat': 19.9975, 'lon': 73.7898}
        }
        
        # Regional language translations for weather conditions
        self.translations = {
            'en': {
                'clear': 'Clear Sky',
                'clouds': 'Cloudy',
                'rain': 'Rain',
                'thunderstorm': 'Thunderstorm',
                'snow': 'Snow',
                'mist': 'Mist',
                'good_farming': 'Good day for farming',
                'avoid_farming': 'Avoid farming activities',
                'irrigation_recommended': 'Irrigation recommended',
                'harvest_weather': 'Good for harvesting'
            },
            'hi': {
                'clear': 'साफ आसमान',
                'clouds': 'बादल',
                'rain': 'बारिश',
                'thunderstorm': 'आंधी-तूफान',
                'snow': 'बर्फबारी',
                'mist': 'कोहरा',
                'good_farming': 'खेती के लिए अच्छा दिन',
                'avoid_farming': 'खेती से बचें',
                'irrigation_recommended': 'सिंचाई की सिफारिश',
                'harvest_weather': 'कटाई के लिए अच्छा'
            },
            'te': {
                'clear': 'స్పష్టమైన ఆకాశం',
                'clouds': 'మేఘావృతం',
                'rain': 'వర్షం',
                'thunderstorm': 'ఉరుములతో కూడిన వర్షం',
                'snow': 'మంచు',
                'mist': 'పొగమంచు',
                'good_farming': 'వ్యవసాయానికి మంచి రోజు',
                'avoid_farming': 'వ్యవసాయ కార్యకలాపాలను నివారించండి',
                'irrigation_recommended': 'నీటిపారుదల సిఫార్సు చేయబడింది',
                'harvest_weather': 'పంట కోతకు మంచిది'
            },
            'ta': {
                'clear': 'தெளிவான வானம்',
                'clouds': 'மேகமூட்டம்',
                'rain': 'மழை',
                'thunderstorm': 'இடி மின்னல்',
                'snow': 'பனி',
                'mist': 'மூடுபனி',
                'good_farming': 'விவசாயத்திற்கு நல்ல நாள்',
                'avoid_farming': 'விவசாய நடவடிக்கைகளை தவிர்க்கவும்',
                'irrigation_recommended': 'நீர்ப்பாசனம் பரிந்துரைக்கப்படுகிறது',
                'harvest_weather': 'அறுவடைக்கு நல்லது'
            }
        }
    
    def get_current_weather(self, city: str = "hyderabad", lang: str = "en", use_cache: bool = True) -> Dict:
        """Get comprehensive current weather data using Open-Meteo API"""
        cache_key = f'weather_current_{city}_{lang}'
        
        # Check cache first (if caching is enabled)
        if use_cache:
            cached_data = cache.get(cache_key)
            if cached_data:
                return cached_data
            
        try:
            coords = self.city_coordinates.get(city.lower(), self.city_coordinates['hyderabad'])
            
            params = {
                'latitude': coords['lat'],
                'longitude': coords['lon'],
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m,wind_direction_10m,pressure_msl',
                'timezone': 'Asia/Kolkata'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            current = data['current']
            
            weather_data = {
                'temperature': round(current['temperature_2m']),
                'apparent_temperature': round(current['apparent_temperature']),
                'description': self._get_weather_description(current['weather_code'], lang),
                'humidity': current['relative_humidity_2m'],
                'wind_speed': round(current['wind_speed_10m'], 1),
                'wind_direction': self._get_wind_direction(current['wind_direction_10m']),
                'pressure': round(current['pressure_msl']),
                'precipitation': current['precipitation'],
                'weather_code': current['weather_code'],
                'city': city.title(),
                'country': 'IN',
                'timestamp': datetime.now().isoformat(),
                'feels_like': round(current['apparent_temperature']),
                'uv_index': self._get_uv_index(current['weather_code']),
                'visibility': self._get_visibility(current['weather_code']),
                'condition': self._get_condition_from_code(current['weather_code']),
                'icon': self._get_weather_icon(current['weather_code']),
                'location': city.title(),
                'sunrise': self._get_sunrise_time(),
                'sunset': self._get_sunset_time()
            }
            
            # Cache for 30 minutes (if caching is enabled)
            if use_cache:
                cache.set(cache_key, weather_data, 1800)
            
            return weather_data
            
        except Exception as e:
            logger.error(f"Open-Meteo API error: {e}")
            return self._get_mock_weather_data(city, lang)
    
    def get_5_day_forecast(self, city: str = "hyderabad", lang: str = "en") -> List[Dict]:
        """Get detailed 5-day weather forecast using Open-Meteo API"""
        cache_key = f'weather_forecast_{city}_{lang}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
            
        try:
            coords = self.city_coordinates.get(city.lower(), self.city_coordinates['hyderabad'])
            
            params = {
                'latitude': coords['lat'],
                'longitude': coords['lon'],
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,relative_humidity_2m_mean',
                'forecast_days': 5,
                'timezone': 'Asia/Kolkata'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            daily = data['daily']
            
            forecasts = []
            for i in range(5):
                date = daily['time'][i]
                forecasts.append({
                    'date': date,
                    'day_name': self._get_day_name(date),
                    'max_temp': round(daily['temperature_2m_max'][i]),
                    'min_temp': round(daily['temperature_2m_min'][i]),
                    'temperature': round((daily['temperature_2m_max'][i] + daily['temperature_2m_min'][i]) / 2),
                    'temp_max': round(daily['temperature_2m_max'][i]),
                    'temp_min': round(daily['temperature_2m_min'][i]),
                    'description': self._get_weather_description(daily['weather_code'][i], lang),
                    'condition': self._get_condition_from_code(daily['weather_code'][i]),
                    'humidity': round(daily['relative_humidity_2m_mean'][i]),
                    'wind_speed': round(daily['wind_speed_10m_max'][i], 1),
                    'precipitation': round(daily['precipitation_sum'][i], 1),
                    'weather_code': daily['weather_code'][i],
                    'icon': self._get_weather_icon(daily['weather_code'][i]),
                    'farming_conditions': self._get_daily_farming_conditions(
                        daily['temperature_2m_max'][i],
                        daily['temperature_2m_min'][i],
                        daily['precipitation_sum'][i],
                        daily['wind_speed_10m_max'][i],
                        daily['weather_code'][i],
                        lang
                    )
                })
            
            # Cache for 1 hour
            cache.set(cache_key, forecasts, 3600)
            
            return forecasts
            
        except Exception as e:
            logger.error(f"Open-Meteo forecast API error: {e}")
            return self._get_mock_forecast_data(city, lang)
    
    def get_farming_recommendations(self, weather_data: Dict, crop_type: str = None, lang: str = "en") -> List[Dict]:
        """Get advanced farming recommendations based on comprehensive weather data"""
        recommendations = []
        trans = self.translations.get(lang, self.translations['en'])
        
        temp = weather_data.get('temperature', 20)
        apparent_temp = weather_data.get('apparent_temperature', temp)
        humidity = weather_data.get('humidity', 50)
        wind_speed = weather_data.get('wind_speed', 5)
        precipitation = weather_data.get('precipitation', 0)
        pressure = weather_data.get('pressure', 1013)
        weather_code = weather_data.get('weather_code', 0)
        
        # Temperature-based recommendations
        if temp > 38:
            recommendations.append({
                'type': 'danger',
                'icon': '🌡️',
                'title': 'Extreme Heat Warning' if lang == 'en' else 'अत्यधिक गर्मी की चेतावनी' if lang == 'hi' else 'అత్యధిక వేడి హెచ్చరిక',
                'message': 'Temperature above 40°C' if lang == 'en' else 'तापमान 40°C से अधिक' if lang == 'hi' else 'ఉష్ణోగ్రత 40°C కంటే ఎక్కువ',
                'action': 'Water crops twice daily, use shade nets' if lang == 'en' else 'दिन में दो बार फसलों को पानी दें, छाया जाल का उपयोग करें' if lang == 'hi' else 'రోజుకు రెండుసార్లు పంటలకు నీరు ఇవ్వండి, నీడ గడ్డలను ఉపయోగించండి'
            })
        elif temp > 35:
            recommendations.append({
                'type': 'warning',
                'icon': '🌡️',
                'title': 'High Temperature Alert' if lang == 'en' else 'उच्च तापमान चेतावनी' if lang == 'hi' else 'అధిక ఉష్ణోగ్రత హెచ్చరిక',
                'message': 'Temperature above 35°C' if lang == 'en' else 'तापमान 35°C से अधिक' if lang == 'hi' else 'ఉష్ణోగ్రత 35°C కంటే ఎక్కువ',
                'action': 'Increase irrigation frequency' if lang == 'en' else 'सिंचाई की आवृत्ति बढ़ाएं' if lang == 'hi' else 'నీటిపారుదల పౌనఃపున్యం పెంచండి'
            })
        elif temp < 15:
            recommendations.append({
                'type': 'warning',
                'icon': '❄️',
                'title': 'Cool Weather Alert' if lang == 'en' else 'ठंड का मौसम चेतावनी' if lang == 'hi' else 'చల్లని వాతావరణ హెచ్చరిక',
                'message': 'Temperature below 15°C' if lang == 'en' else 'तापमान 15°C से कम' if lang == 'hi' else 'ఉష్ణోగ్రత 15°C కంటే తక్కువ',
                'action': 'Reduce irrigation frequency' if lang == 'en' else 'सिंचाई की आवृत्ति कम करें' if lang == 'hi' else 'నీటిపారుదల పౌనఃపున్యం తగ్గించండి'
            })
        elif temp < 10:
            recommendations.append({
                'type': 'danger',
                'icon': '❄️',
                'title': 'Cold Warning' if lang == 'en' else 'ठंड की चेतावनी' if lang == 'hi' else 'చలి హెచ్చరిక',
                'message': 'Temperature below 10°C' if lang == 'en' else 'तापमान 10°C से कम' if lang == 'hi' else 'ఉష్ణోగ్రత 10°C కంటే తక్కువ',
                'action': 'Protect sensitive crops immediately' if lang == 'en' else 'संवेदनशील फसलों की तुरंत रक्षा करें' if lang == 'hi' else 'సున్నితమైన పంటలను వెంటనే రక్షించండి'
            })
        
        # Humidity recommendations
        if humidity > 85:
            recommendations.append({
                'type': 'warning',
                'icon': '💧',
                'title': 'Very High Humidity' if lang == 'en' else 'बहुत अधिक आर्द्रता' if lang == 'hi' else 'అత్యధిక తేమ',
                'message': 'Humidity above 85%' if lang == 'en' else 'आर्द्रता 85% से अधिक' if lang == 'hi' else 'తేమ 85% కంటే ఎక్కువ',
                'action': 'High disease risk - improve air circulation' if lang == 'en' else 'उच्च रोग जोखिम - वायु परिसंचरण में सुधार करें' if lang == 'hi' else 'అధిక వ్యాధి ప్రమాదం - గాలి ప్రసరణను మెరుగుపరచండి'
            })
        elif humidity < 30:
            recommendations.append({
                'type': 'warning',
                'icon': '🏜️',
                'title': 'Very Low Humidity' if lang == 'en' else 'बहुत कम आर्द्रता' if lang == 'hi' else 'అత్యల్ప తేమ',
                'message': 'Humidity below 30%' if lang == 'en' else 'आर्द्रता 30% से कम' if lang == 'hi' else 'తేమ 30% కంటే తక్కువ',
                'action': 'High irrigation demand - mulch heavily' if lang == 'en' else 'उच्च सिंचाई मांग - भारी मल्चिंग करें' if lang == 'hi' else 'అధిక నీటిపారుదల డిమాండ్ - బరువైన మల్చింగ్ చేయండి'
            })
        
        # Wind recommendations
        if wind_speed > 20:
            recommendations.append({
                'type': 'danger',
                'icon': '💨',
                'title': 'Strong Winds' if lang == 'en' else 'तेज़ हवाएं' if lang == 'hi' else 'బలమైన గాలులు',
                'message': f'Wind speed {wind_speed} km/h' if lang == 'en' else f'हवा की गति {wind_speed} किमी/घंटा' if lang == 'hi' else f'గాలి వేగం {wind_speed} కిమీ/గం',
                'action': 'Secure all structures immediately' if lang == 'en' else 'सभी संरचनाओं को तुरंत सुरक्षित करें' if lang == 'hi' else 'అన్ని నిర్మాణాలను వెంటనే సురక్షితంగా ఉంచండి'
            })
        elif wind_speed > 15:
            recommendations.append({
                'type': 'warning',
                'icon': '💨',
                'title': 'Moderate Winds' if lang == 'en' else 'मध्यम हवाएं' if lang == 'hi' else 'మధ్యస్థ గాలులు',
                'message': f'Wind speed {wind_speed} km/h' if lang == 'en' else f'हवा की गति {wind_speed} किमी/घंटा' if lang == 'hi' else f'గాలి వేగం {wind_speed} కిమీ/గం',
                'action': 'Secure greenhouse covers' if lang == 'en' else 'ग्रीनहाउस कवर को सुरक्षित करें' if lang == 'hi' else 'గ్రీన్ హౌస్ కవర్లను సురక్షితంగా ఉంచండి'
            })
        
        # Precipitation recommendations
        if precipitation > 10:
            recommendations.append({
                'type': 'danger',
                'icon': '🌧️',
                'title': 'Heavy Rain Alert' if lang == 'en' else 'भारी बारिश की चेतावनी' if lang == 'hi' else 'భారీ వర్షం హెచ్చరిక',
                'message': f'Heavy rain expected: {precipitation}mm' if lang == 'en' else f'भारी बारिश की उम्मीद: {precipitation}मिमी' if lang == 'hi' else f'భారీ వర్షం అంచనా: {precipitation}మిమీ',
                'action': 'Clear drainage channels, avoid field work' if lang == 'en' else 'जल निकासी नालियां साफ करें, खेत का काम न करें' if lang == 'hi' else 'జలనిక్షేపణ ఛానెల్లను శుభ్రపరచండి, పొలం పనిని నివారించండి'
            })
        elif precipitation > 5:
            recommendations.append({
                'type': 'info',
                'icon': '🌧️',
                'title': 'Moderate Rain' if lang == 'en' else 'मध्यम बारिश' if lang == 'hi' else 'మధ్యస్థ వర్షం',
                'message': f'Rain expected: {precipitation}mm' if lang == 'en' else f'बारिश की उम्मीद: {precipitation}मिमी' if lang == 'hi' else f'వర్షం అంచనా: {precipitation}మిమీ',
                'action': 'Good for soil moisture, reduce irrigation' if lang == 'en' else 'मिट्टी की नमी के लिए अच्छा, सिंचाई कम करें' if lang == 'hi' else 'మట్టి తేమకు మంచిది, నీటిపారుదల తగ్గించండి'
            })
        
        # Good farming weather
        if 20 <= temp <= 30 and weather_code in [0, 1, 2] and wind_speed < 15 and humidity < 70:
            recommendations.append({
                'type': 'success',
                'icon': '☀️',
                'title': trans.get('good_farming', 'Good day for farming'),
                'message': 'Ideal conditions for farming activities' if lang == 'en' else 'खेती की गतिविधियों के लिए आदर्श स्थिति' if lang == 'hi' else 'వ్యవసాయ కార్యకలాపాలకు అనువైన పరిస్థితులు',
                'action': 'Perfect for planting, spraying, and field work' if lang == 'en' else 'रोपण, छिड़काव और खेत के काम के लिए आदर्श' if lang == 'hi' else 'నాటడం, పిచికారీ మరియు పొలం పనికి అనువైనది'
            })
        
        return recommendations[:6]  # Limit to 6 most important recommendations
    
    def get_weather_alerts(self, city: str = "hyderabad", lang: str = "en") -> List[Dict]:
        """Get weather alerts and warnings for farmers"""
        current_weather = self.get_current_weather(city, lang)
        alerts = []
        
        temp = current_weather.get('temperature', 20)
        wind_speed = current_weather.get('wind_speed', 5)
        precipitation = current_weather.get('precipitation', 0)
        humidity = current_weather.get('humidity', 50)
        weather_code = current_weather.get('weather_code', 0)
        
        # Temperature alerts
        if temp > 40:
            alerts.append({
                'type': 'extreme_heat',
                'level': 'danger',
                'icon': '🌡️',
                'message': 'Extreme Heat Warning - Temperature above 40°C' if lang == 'en' else 'अत्यधिक गर्मी की चेतावनी - तापमान 40°C से अधिक' if lang == 'hi' else 'అత్యధిక వేడి హెచ్చరిక - ఉష్ణోగ్రత 40°C కంటే ఎక్కువ',
                'recommendation': 'Water crops immediately and provide shade' if lang == 'en' else 'फसलों को तुरंत पानी दें और छाया प्रदान करें' if lang == 'hi' else 'పంటలకు వెంటనే నీరు ఇవ్వండి మరియు నీడ అందించండి'
            })
        elif temp > 35:
            alerts.append({
                'type': 'heat_warning',
                'level': 'warning',
                'icon': '🌡️',
                'message': 'High Temperature Alert - Above 35°C' if lang == 'en' else 'उच्च तापमान चेतावनी - 35°C से अधिक' if lang == 'hi' else 'అధిక ఉష్ణోగ్రత హెచ్చరిక - 35°C కంటే ఎక్కువ',
                'recommendation': 'Increase irrigation frequency' if lang == 'en' else 'सिंचाई की आवृत्ति बढ़ाएं' if lang == 'hi' else 'నీటిపారుదల పౌనఃపున్యం పెంచండి'
            })
        elif temp < 5:
            alerts.append({
                'type': 'frost_warning',
                'level': 'danger',
                'icon': '❄️',
                'message': 'Frost Warning - Temperature below 5°C' if lang == 'en' else 'पाले की चेतावनी - तापमान 5°C से कम' if lang == 'hi' else 'మంచు హెచ్చరిక - ఉష్ణోగ్రత 5°C కంటే తక్కువ',
                'recommendation': 'Protect crops with covers immediately' if lang == 'en' else 'फसलों को तुरंत कवर से बचाएं' if lang == 'hi' else 'పంటలను వెంటనే కవర్లతో రక్షించండి'
            })
        
        # Wind alerts
        if wind_speed > 25:
            alerts.append({
                'type': 'strong_wind',
                'level': 'danger',
                'icon': '💨',
                'message': f'Strong Wind Alert - {wind_speed} km/h' if lang == 'en' else f'तेज़ हवा की चेतावनी - {wind_speed} किमी/घंटा' if lang == 'hi' else f'బలమైన గాలి హెచ్చరిక - {wind_speed} కిమీ/గం',
                'recommendation': 'Secure all farm structures and equipment' if lang == 'en' else 'सभी खेत संरचनाओं और उपकरणों को सुरक्षित करें' if lang == 'hi' else 'అన్ని వ్యవసాయ నిర్మాణాలు మరియు పరికరాలను సురక్షితంగా ఉంచండి'
            })
        elif wind_speed > 15:
            alerts.append({
                'type': 'moderate_wind',
                'level': 'warning',
                'icon': '💨',
                'message': f'Moderate Winds - {wind_speed} km/h' if lang == 'en' else f'मध्यम हवाएं - {wind_speed} किमी/घंटा' if lang == 'hi' else f'మధ్యస్థ గాలులు - {wind_speed} కిమీ/గం',
                'recommendation': 'Check greenhouse covers and crop supports' if lang == 'en' else 'ग्रीनहाउस कवर और फसल समर्थन की जांच करें' if lang == 'hi' else 'గ్రీన్ హౌస్ కవర్లు మరియు పంట మద్దతులను తనిఖీ చేయండి'
            })
        
        # Precipitation alerts
        if precipitation > 15:
            alerts.append({
                'type': 'heavy_rain',
                'level': 'danger',
                'icon': '🌧️',
                'message': 'Heavy Rainfall Alert' if lang == 'en' else 'भारी बारिश की चेतावनी' if lang == 'hi' else 'భారీ వర్షపాతం హెచ్చరిక',
                'recommendation': 'Clear drainage and avoid field operations' if lang == 'en' else 'जल निकासी साफ करें और खेत के काम से बचें' if lang == 'hi' else 'జలనిక్షేపణ శుభ్రపరచండి మరియు పొలం కార్యకలాపాలను నివారించండి'
            })
        
        # Humidity alerts
        if humidity > 90:
            alerts.append({
                'type': 'high_humidity',
                'level': 'warning',
                'icon': '💧',
                'message': 'Very High Humidity - Disease Risk' if lang == 'en' else 'बहुत अधिक आर्द्रता - रोग जोखिम' if lang == 'hi' else 'అత్యధిక తేమ - వ్యాధి ప్రమాదం',
                'recommendation': 'Monitor crops for fungal infections' if lang == 'en' else 'फफूंदी संक्रमण के लिए फसलों की निगरानी करें' if lang == 'hi' else 'పుట్టు సోకిన వ్యాధుల కోసం పంటలను పర్యవేక్షించండి'
            })
        
        return alerts
    
    def _get_weather_description(self, code: int, lang: str = "en") -> str:
        """Convert weather code to description in specified language"""
        weather_codes = {
            'en': {
                0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
                45: "Fog", 48: "Depositing rime fog", 51: "Light drizzle", 53: "Moderate drizzle",
                55: "Dense drizzle", 56: "Light freezing drizzle", 57: "Dense freezing drizzle",
                61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
                66: "Light freezing rain", 67: "Heavy freezing rain",
                71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
                77: "Snow grains", 80: "Slight rain showers", 81: "Moderate rain showers",
                82: "Violent rain showers", 85: "Slight snow showers", 86: "Heavy snow showers",
                95: "Thunderstorm", 96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
            },
            'hi': {
                0: "साफ आसमान", 1: "मुख्य रूप से साफ", 2: "आंशिक रूप से बादल", 3: "बादल छाए",
                45: "कोहरा", 48: "जमा हुआ कोहरा", 51: "हल्की बूंदाबांदी", 53: "मध्यम बूंदाबांदी",
                55: "घनी बूंदाबांदी", 56: "हल्की जमने वाली बूंदाबांदी", 57: "घनी जमने वाली बूंदाबांदी",
                61: "हल्की बारिश", 63: "मध्यम बारिश", 65: "भारी बारिश",
                66: "हल्की जमने वाली बारिश", 67: "भारी जमने वाली बारिश",
                71: "हल्की बर्फबारी", 73: "मध्यम बर्फबारी", 75: "भारी बर्फबारी",
                77: "बर्फ के दाने", 80: "हल्की बारिश की बौछारें", 81: "मध्यम बारिश की बौछारें",
                82: "तेज़ बारिश की बौछारें", 85: "हल्की बर्फ की बौछारें", 86: "भारी बर्फ की बौछारें",
                95: "आंधी-तूफान", 96: "हल्के ओलों के साथ आंधी", 99: "भारी ओलों के साथ आंधी"
            },
            'te': {
                0: "స్పష్టమైన ఆకాశం", 1: "ప్రధానంగా స్పష్టం", 2: "ఆంశికంగా మేఘావృతం", 3: "మేఘావృతం",
                45: "పొగమంచు", 48: "గడ్డకట్టిన పొగమంచు", 51: "తేలికపాటి మబ్బు", 53: "మధ్యస్థ మబ్బు",
                55: "భారీ మబ్బు", 56: "తేలికపాటి గడ్డకట్టే మబ్బు", 57: "భారీ గడ్డకట్టే మబ్బు",
                61: "తేలికపాటి వర్షం", 63: "మధ్యస్థ వర్షం", 65: "భారీ వర్షం",
                66: "తేలికపాటి గడ్డకట్టే వర్షం", 67: "భారీ గడ్డకట్టే వర్షం",
                71: "తేలికపాటి మంచు", 73: "మధ్యస్థ మంచు", 75: "భారీ మంచు",
                77: "మంచు రేణువులు", 80: "తేలికపాటి వర్షపాతం", 81: "మధ్యస్థ వర్షపాతం",
                82: "భారీ వర్షపాతం", 85: "తేలికపాటి మంచు పాతం", 86: "భారీ మంచు పాతం",
                95: "ఉరుములతో కూడిన వర్షం", 96: "తేలికపాటి వడగండ్లతో ఉరుములు", 99: "భారీ వడగండ్లతో ఉరుములు"
            }
        }
        
        lang_codes = weather_codes.get(lang, weather_codes['en'])
        return lang_codes.get(code, "Unknown")
    
    def _get_condition_from_code(self, code: int) -> str:
        """Get condition category from weather code"""
        if code == 0:
            return "Clear"
        elif code in [1, 2, 3]:
            return "Clouds"
        elif code in [45, 48]:
            return "Mist"
        elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
            return "Rain"
        elif code in [71, 73, 75, 77, 85, 86]:
            return "Snow"
        elif code in [95, 96, 99]:
            return "Thunderstorm"
        else:
            return "Clear"
    
    def _get_wind_direction(self, degrees: float) -> str:
        """Convert wind direction degrees to compass direction"""
        directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                     'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        index = round(degrees / 22.5) % 16
        return directions[index]
    
    def _get_uv_index(self, weather_code: int) -> str:
        """Estimate UV index based on weather conditions"""
        if weather_code == 0:  # Clear sky
            return "High (8-10)"
        elif weather_code in [1, 2]:  # Mainly clear, partly cloudy
            return "Moderate (5-7)"
        elif weather_code == 3:  # Overcast
            return "Low (2-4)"
        else:
            return "Very Low (0-2)"
    
    def _get_visibility(self, weather_code: int) -> str:
        """Estimate visibility based on weather conditions"""
        if weather_code in [45, 48]:  # Fog
            return "Poor (0-1 km)"
        elif weather_code in [71, 73, 75, 77]:  # Snow
            return "Reduced (1-5 km)"
        elif weather_code in [51, 53, 55, 61, 63, 65]:  # Rain
            return "Moderate (5-10 km)"
        else:
            return "Good (10+ km)"
    
    def _get_weather_icon(self, weather_code: int) -> str:
        """Get weather icon based on weather code"""
        icon_map = {
            0: "01d", 1: "02d", 2: "02d", 3: "04d",
            45: "50d", 48: "50d", 51: "09d", 53: "09d", 55: "09d",
            56: "13d", 57: "13d", 61: "10d", 63: "10d", 65: "10d",
            66: "13d", 67: "13d", 71: "13d", 73: "13d", 75: "13d",
            77: "13d", 80: "09d", 81: "09d", 82: "09d",
            85: "13d", 86: "13d", 95: "11d", 96: "11d", 99: "11d"
        }
        return icon_map.get(weather_code, "01d")
    
    def _get_day_name(self, date_str: str) -> str:
        """Get day name from date string"""
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%A')
    
    def _get_sunrise_time(self) -> datetime:
        """Get approximate sunrise time"""
        return datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    
    def _get_sunset_time(self) -> datetime:
        """Get approximate sunset time"""
        return datetime.now().replace(hour=18, minute=30, second=0, microsecond=0)
    
    def _get_daily_farming_conditions(self, max_temp: float, min_temp: float, 
                                    precipitation: float, wind_speed: float, weather_code: int, lang: str = "en") -> str:
        """Get farming conditions assessment for the day"""
        conditions = {
            'en': {
                'wet': 'Wet - Avoid field work',
                'hot': 'Hot - Extra irrigation needed',
                'cold': 'Cold - Protect sensitive crops',
                'windy': 'Windy - Secure structures',
                'excellent': 'Excellent - Perfect for field work',
                'good': 'Good - Suitable for most activities',
                'moderate': 'Moderate - Check specific conditions'
            },
            'hi': {
                'wet': 'गीला - खेत का काम न करें',
                'hot': 'गर्म - अतिरिक्त सिंचाई की आवश्यकता',
                'cold': 'ठंडा - संवेदनशील फसलों की रक्षा करें',
                'windy': 'हवादार - संरचनाओं को सुरक्षित करें',
                'excellent': 'उत्कृष्ट - खेत के काम के लिए आदर्श',
                'good': 'अच्छा - अधिकांश गतिविधियों के लिए उपयुक्त',
                'moderate': 'मध्यम - विशिष्ट स्थितियों की जांच करें'
            },
            'te': {
                'wet': 'తడి - పొలం పనిని నివారించండి',
                'hot': 'వేడి - అదనపు నీటిపారుదల అవసరం',
                'cold': 'చలి - సున్నితమైన పంటలను రక్షించండి',
                'windy': 'గాలి - నిర్మాణాలను సురక్షితంగా ఉంచండి',
                'excellent': 'అద్భుతమైన - పొలం పనికి అనువైనది',
                'good': 'మంచిది - చాలా కార్యకలాపాలకు అనువైనది',
                'moderate': 'మధ్యస్థ - నిర్దిష్ట పరిస్థితులను తనిఖీ చేయండి'
            }
        }
        
        lang_conditions = conditions.get(lang, conditions['en'])
        
        if precipitation > 10:
            return lang_conditions['wet']
        elif max_temp > 38:
            return lang_conditions['hot']
        elif min_temp < 10:
            return lang_conditions['cold']
        elif wind_speed > 20:
            return lang_conditions['windy']
        elif weather_code == 0:
            return lang_conditions['excellent']
        elif weather_code in [1, 2]:
            return lang_conditions['good']
        else:
            return lang_conditions['moderate']
    
    def _get_mock_weather_data(self, city: str = "hyderabad", lang: str = "en") -> Dict:
        """Return mock weather data when API is not available"""
        return {
            'temperature': 28,
            'apparent_temperature': 30,
            'description': self._get_weather_description(2, lang),
            'humidity': 65,
            'wind_speed': 8.5,
            'wind_direction': 'NE',
            'pressure': 1013,
            'precipitation': 0,
            'weather_code': 2,
            'city': city.title(),
            'country': 'IN',
            'timestamp': datetime.now().isoformat(),
            'feels_like': 30,
            'uv_index': 'Moderate (5-7)',
            'visibility': 'Good (10+ km)',
            'condition': 'Clouds',
            'icon': '02d',
            'location': city.title(),
            'sunrise': self._get_sunrise_time(),
            'sunset': self._get_sunset_time(),
            'is_fallback': True
        }
    
    def _get_mock_forecast_data(self, city: str = "hyderabad", lang: str = "en") -> List[Dict]:
        """Return mock forecast data when API is not available"""
        forecasts = []
        base_date = datetime.now()
        
        weather_codes = [0, 2, 3, 61, 63]
        farming_conditions = ['excellent', 'good', 'moderate', 'wet', 'good']
        
        for i in range(5):
            date = (base_date + timedelta(days=i)).strftime('%Y-%m-%d')
            weather_code = weather_codes[i % len(weather_codes)]
            forecasts.append({
                'date': date,
                'day_name': (base_date + timedelta(days=i)).strftime('%A'),
                'max_temp': 30 + (i % 3),
                'min_temp': 20 + (i % 2),
                'temperature': 25 + (i % 2),
                'temp_max': 30 + (i % 3),
                'temp_min': 20 + (i % 2),
                'description': self._get_weather_description(weather_code, lang),
                'condition': self._get_condition_from_code(weather_code),
                'humidity': 60 + (i * 5),
                'wind_speed': 5.0 + (i * 0.5),
                'precipitation': 0 if i % 2 == 0 else 2.5,
                'weather_code': weather_code,
                'icon': self._get_weather_icon(weather_code),
                'farming_conditions': self._get_daily_farming_conditions(30, 20, 0, 5, weather_code, lang)
            })
        
        return forecasts


# Initialize advanced weather service
advanced_weather_service = AdvancedWeatherService()

# Legacy compatibility
WeatherService = AdvancedWeatherService
weather_service = advanced_weather_service
