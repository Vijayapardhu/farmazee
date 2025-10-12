"""
Enhanced Weather Services with Real-Time Data and Regional Language Support
"""
import requests
import os
from datetime import datetime, timedelta
from django.core.cache import cache
from django.utils import timezone


class WeatherService:
    """
    Hyperlocal weather service with regional language support
    Uses OpenWeatherMap API for real-time data
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY', 'demo_key')
        self.base_url = 'https://api.openweathermap.org/data/2.5'
        
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
            },
            'mr': {
                'clear': 'स्वच्छ आकाश',
                'clouds': 'ढगाळ',
                'rain': 'पाऊस',
                'thunderstorm': 'वादळी वीज',
                'snow': 'बर्फ',
                'mist': 'धुके',
                'good_farming': 'शेतीसाठी चांगला दिवस',
                'avoid_farming': 'शेती टाळा',
                'irrigation_recommended': 'सिंचनाची शिफारस',
                'harvest_weather': 'कापणीसाठी चांगले'
            }
        }
    
    def get_current_weather(self, lat, lon, lang='en'):
        """
        Get current weather for specific coordinates
        """
        cache_key = f'weather_current_{lat}_{lon}_{lang}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f'{self.base_url}/weather'
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',
                'lang': lang
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            weather_data = self._process_current_weather(data, lang)
            
            # Cache for 30 minutes
            cache.set(cache_key, weather_data, 1800)
            
            return weather_data
            
        except Exception as e:
            return self._get_fallback_weather(lang)
    
    def get_forecast(self, lat, lon, days=7, lang='en'):
        """
        Get weather forecast for next N days
        """
        cache_key = f'weather_forecast_{lat}_{lon}_{days}_{lang}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return cached_data
        
        try:
            url = f'{self.base_url}/forecast'
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'units': 'metric',
                'lang': lang
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            forecast_data = self._process_forecast(data, days, lang)
            
            # Cache for 1 hour
            cache.set(cache_key, forecast_data, 3600)
            
            return forecast_data
            
        except Exception as e:
            return self._get_fallback_forecast(days, lang)
    
    def get_weather_alerts(self, lat, lon, lang='en'):
        """
        Get weather alerts and warnings
        """
        try:
            url = f'{self.base_url}/onecall'
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.api_key,
                'exclude': 'minutely,hourly',
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            alerts = []
            if 'alerts' in data:
                for alert in data['alerts']:
                    alerts.append({
                        'event': alert.get('event'),
                        'description': alert.get('description'),
                        'start': datetime.fromtimestamp(alert.get('start')),
                        'end': datetime.fromtimestamp(alert.get('end')),
                        'severity': self._determine_severity(alert),
                        'farming_impact': self._get_farming_impact(alert, lang)
                    })
            
            return alerts
            
        except Exception:
            return []
    
    def get_farming_recommendations(self, weather_data, crop_type=None, lang='en'):
        """
        Get farming recommendations based on weather
        """
        recommendations = []
        trans = self.translations.get(lang, self.translations['en'])
        
        temp = weather_data.get('temperature', 25)
        condition = weather_data.get('condition', 'clear').lower()
        humidity = weather_data.get('humidity', 50)
        wind_speed = weather_data.get('wind_speed', 5)
        
        # Temperature-based recommendations
        if temp > 35:
            recommendations.append({
                'type': 'warning',
                'message': 'High temperature alert' if lang == 'en' else 'उच्च तापमान चेतावनी' if lang == 'hi' else 'అధిక ఉష్ణోగ్రత హెచ్చరిక',
                'action': 'Ensure adequate irrigation' if lang == 'en' else 'पर्याप्त सिंचाई सुनिश्चित करें' if lang == 'hi' else 'తగినంత నీటిపారుదల నిర్ధారించండి'
            })
        elif temp < 10:
            recommendations.append({
                'type': 'warning',
                'message': 'Low temperature alert' if lang == 'en' else 'कम तापमान चेतावनी' if lang == 'hi' else 'తక్కువ ఉష్ణోగ్రత హెచ్చరిక',
                'action': 'Protect sensitive crops' if lang == 'en' else 'संवेदनशील फसलों की रक्षा करें' if lang == 'hi' else 'సున్నితమైన పంటలను రక్షించండి'
            })
        
        # Rain-based recommendations
        if 'rain' in condition:
            recommendations.append({
                'type': 'info',
                'message': 'Rain expected' if lang == 'en' else 'बारिश की उम्मीद' if lang == 'hi' else 'వర్షం అంచనా',
                'action': 'Skip irrigation, protect harvested crops' if lang == 'en' else 'सिंचाई छोड़ें, कटाई की फसलों की रक्षा करें' if lang == 'hi' else 'నీటిపారుదల వదులుకోండి, కోసిన పంటలను రక్షించండి'
            })
        elif humidity < 30:
            recommendations.append({
                'type': 'info',
                'message': trans.get('irrigation_recommended', 'Irrigation recommended'),
                'action': 'Plan irrigation for today' if lang == 'en' else 'आज के लिए सिंचाई की योजना बनाएं' if lang == 'hi' else 'ఈరోజు నీటిపారుదల ప్రణాళిక చేయండి'
            })
        
        # Good farming weather
        if 20 <= temp <= 30 and 'clear' in condition and wind_speed < 15:
            recommendations.append({
                'type': 'success',
                'message': trans.get('good_farming', 'Good day for farming'),
                'action': 'Ideal for planting and field activities' if lang == 'en' else 'रोपण और खेत की गतिविधियों के लिए आदर्श' if lang == 'hi' else 'నాటడం మరియు పొలం కార్యకలాపాలకు అనువైనది'
            })
        
        return recommendations
    
    def _process_current_weather(self, data, lang):
        """Process API response for current weather"""
        return {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind'].get('deg', 0),
            'clouds': data['clouds']['all'],
            'visibility': data.get('visibility', 10000) / 1000,  # km
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']),
            'location': data['name'],
            'timestamp': datetime.fromtimestamp(data['dt'])
        }
    
    def _process_forecast(self, data, days, lang):
        """Process API response for forecast"""
        forecast_list = []
        processed_dates = set()
        
        for item in data['list'][:days * 8]:  # 8 readings per day
            date = datetime.fromtimestamp(item['dt']).date()
            
            if date not in processed_dates:
                forecast_list.append({
                    'date': date,
                    'temperature': item['main']['temp'],
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'condition': item['weather'][0]['main'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed'],
                    'rain_probability': item.get('pop', 0) * 100
                })
                processed_dates.add(date)
        
        return forecast_list
    
    def _get_fallback_weather(self, lang):
        """Fallback weather data when API fails"""
        return {
            'temperature': 28,
            'feels_like': 30,
            'temp_min': 24,
            'temp_max': 32,
            'humidity': 65,
            'pressure': 1013,
            'condition': 'Clear',
            'description': 'Partly cloudy',
            'icon': '02d',
            'wind_speed': 8,
            'wind_direction': 180,
            'clouds': 20,
            'visibility': 10,
            'sunrise': datetime.now().replace(hour=6, minute=0),
            'sunset': datetime.now().replace(hour=18, minute=30),
            'location': 'Your Location',
            'timestamp': datetime.now(),
            'is_fallback': True
        }
    
    def _get_fallback_forecast(self, days, lang):
        """Fallback forecast data"""
        forecast = []
        for i in range(days):
            date = datetime.now().date() + timedelta(days=i)
            forecast.append({
                'date': date,
                'temperature': 28 + i,
                'temp_min': 22 + i,
                'temp_max': 33 + i,
                'condition': 'Partly Cloudy',
                'description': 'Partly cloudy',
                'icon': '02d',
                'humidity': 65 - (i * 2),
                'wind_speed': 8,
                'rain_probability': 20
            })
        return forecast
    
    def _determine_severity(self, alert):
        """Determine alert severity"""
        event = alert.get('event', '').lower()
        if any(word in event for word in ['severe', 'extreme', 'emergency']):
            return 'high'
        elif any(word in event for word in ['warning', 'watch']):
            return 'medium'
        return 'low'
    
    def _get_farming_impact(self, alert, lang):
        """Get farming impact description for alert"""
        event = alert.get('event', '').lower()
        
        impacts = {
            'en': {
                'thunderstorm': 'Postpone field activities, secure equipment',
                'rain': 'Skip irrigation, protect harvested crops',
                'wind': 'Secure structures, protect young plants',
                'heat': 'Increase irrigation, provide shade for sensitive crops',
                'cold': 'Protect frost-sensitive crops, delay planting'
            },
            'hi': {
                'thunderstorm': 'खेत की गतिविधियों को स्थगित करें, उपकरण सुरक्षित करें',
                'rain': 'सिंचाई छोड़ें, कटाई की फसलों की रक्षा करें',
                'wind': 'संरचनाओं को सुरक्षित करें, युवा पौधों की रक्षा करें',
                'heat': 'सिंचाई बढ़ाएं, संवेदनशील फसलों के लिए छाया प्रदान करें',
                'cold': 'पाले-संवेदनशील फसलों की रक्षा करें, रोपण में देरी करें'
            },
            'te': {
                'thunderstorm': 'పొలం కార్యకలాపాలను వాయిదా వేయండి, పరికరాలను సురక్షితంగా ఉంచండి',
                'rain': 'నీటిపారుదల వదులుకోండి, కోసిన పంటలను రక్షించండి',
                'wind': 'నిర్మాణాలను సురక్షితంగా ఉంచండి, చిన్న మొక్కలను రక్షించండి',
                'heat': 'నీటిపారుదల పెంచండి, సున్నితమైన పంటలకు నీడ అందించండి',
                'cold': 'మంచుకు సున్నితమైన పంటలను రక్షించండి, నాటడం ఆలస్యం చేయండి'
            }
        }
        
        lang_impacts = impacts.get(lang, impacts['en'])
        
        for key, impact in lang_impacts.items():
            if key in event:
                return impact
        
        return 'Monitor weather conditions closely' if lang == 'en' else 'मौसम की स्थिति की बारीकी से निगरानी करें' if lang == 'hi' else 'వాతావరణ పరిస్థితులను నిశితంగా పర్యవేక్షించండి'


# Initialize weather service
weather_service = WeatherService()

                'message': 'Rain expected' if lang == 'en' else 'बारिश की उम्मीद' if lang == 'hi' else 'వర్షం అంచనా',
                'action': 'Skip irrigation, protect harvested crops' if lang == 'en' else 'सिंचाई छोड़ें, कटाई की फसलों की रक्षा करें' if lang == 'hi' else 'నీటిపారుదల వదులుకోండి, కోసిన పంటలను రక్షించండి'
            })
        elif humidity < 30:
            recommendations.append({
                'type': 'info',
                'message': trans.get('irrigation_recommended', 'Irrigation recommended'),
                'action': 'Plan irrigation for today' if lang == 'en' else 'आज के लिए सिंचाई की योजना बनाएं' if lang == 'hi' else 'ఈరోజు నీటిపారుదల ప్రణాళిక చేయండి'
            })
        
        # Good farming weather
        if 20 <= temp <= 30 and 'clear' in condition and wind_speed < 15:
            recommendations.append({
                'type': 'success',
                'message': trans.get('good_farming', 'Good day for farming'),
                'action': 'Ideal for planting and field activities' if lang == 'en' else 'रोपण और खेत की गतिविधियों के लिए आदर्श' if lang == 'hi' else 'నాటడం మరియు పొలం కార్యకలాపాలకు అనువైనది'
            })
        
        return recommendations
    
    def _process_current_weather(self, data, lang):
        """Process API response for current weather"""
        return {
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'temp_min': data['main']['temp_min'],
            'temp_max': data['main']['temp_max'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
            'condition': data['weather'][0]['main'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'wind_speed': data['wind']['speed'],
            'wind_direction': data['wind'].get('deg', 0),
            'clouds': data['clouds']['all'],
            'visibility': data.get('visibility', 10000) / 1000,  # km
            'sunrise': datetime.fromtimestamp(data['sys']['sunrise']),
            'sunset': datetime.fromtimestamp(data['sys']['sunset']),
            'location': data['name'],
            'timestamp': datetime.fromtimestamp(data['dt'])
        }
    
    def _process_forecast(self, data, days, lang):
        """Process API response for forecast"""
        forecast_list = []
        processed_dates = set()
        
        for item in data['list'][:days * 8]:  # 8 readings per day
            date = datetime.fromtimestamp(item['dt']).date()
            
            if date not in processed_dates:
                forecast_list.append({
                    'date': date,
                    'temperature': item['main']['temp'],
                    'temp_min': item['main']['temp_min'],
                    'temp_max': item['main']['temp_max'],
                    'condition': item['weather'][0]['main'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon'],
                    'humidity': item['main']['humidity'],
                    'wind_speed': item['wind']['speed'],
                    'rain_probability': item.get('pop', 0) * 100
                })
                processed_dates.add(date)
        
        return forecast_list
    
    def _get_fallback_weather(self, lang):
        """Fallback weather data when API fails"""
        return {
            'temperature': 28,
            'feels_like': 30,
            'temp_min': 24,
            'temp_max': 32,
            'humidity': 65,
            'pressure': 1013,
            'condition': 'Clear',
            'description': 'Partly cloudy',
            'icon': '02d',
            'wind_speed': 8,
            'wind_direction': 180,
            'clouds': 20,
            'visibility': 10,
            'sunrise': datetime.now().replace(hour=6, minute=0),
            'sunset': datetime.now().replace(hour=18, minute=30),
            'location': 'Your Location',
            'timestamp': datetime.now(),
            'is_fallback': True
        }
    
    def _get_fallback_forecast(self, days, lang):
        """Fallback forecast data"""
        forecast = []
        for i in range(days):
            date = datetime.now().date() + timedelta(days=i)
            forecast.append({
                'date': date,
                'temperature': 28 + i,
                'temp_min': 22 + i,
                'temp_max': 33 + i,
                'condition': 'Partly Cloudy',
                'description': 'Partly cloudy',
                'icon': '02d',
                'humidity': 65 - (i * 2),
                'wind_speed': 8,
                'rain_probability': 20
            })
        return forecast
    
    def _determine_severity(self, alert):
        """Determine alert severity"""
        event = alert.get('event', '').lower()
        if any(word in event for word in ['severe', 'extreme', 'emergency']):
            return 'high'
        elif any(word in event for word in ['warning', 'watch']):
            return 'medium'
        return 'low'
    
    def _get_farming_impact(self, alert, lang):
        """Get farming impact description for alert"""
        event = alert.get('event', '').lower()
        
        impacts = {
            'en': {
                'thunderstorm': 'Postpone field activities, secure equipment',
                'rain': 'Skip irrigation, protect harvested crops',
                'wind': 'Secure structures, protect young plants',
                'heat': 'Increase irrigation, provide shade for sensitive crops',
                'cold': 'Protect frost-sensitive crops, delay planting'
            },
            'hi': {
                'thunderstorm': 'खेत की गतिविधियों को स्थगित करें, उपकरण सुरक्षित करें',
                'rain': 'सिंचाई छोड़ें, कटाई की फसलों की रक्षा करें',
                'wind': 'संरचनाओं को सुरक्षित करें, युवा पौधों की रक्षा करें',
                'heat': 'सिंचाई बढ़ाएं, संवेदनशील फसलों के लिए छाया प्रदान करें',
                'cold': 'पाले-संवेदनशील फसलों की रक्षा करें, रोपण में देरी करें'
            },
            'te': {
                'thunderstorm': 'పొలం కార్యకలాపాలను వాయిదా వేయండి, పరికరాలను సురక్షితంగా ఉంచండి',
                'rain': 'నీటిపారుదల వదులుకోండి, కోసిన పంటలను రక్షించండి',
                'wind': 'నిర్మాణాలను సురక్షితంగా ఉంచండి, చిన్న మొక్కలను రక్షించండి',
                'heat': 'నీటిపారుదల పెంచండి, సున్నితమైన పంటలకు నీడ అందించండి',
                'cold': 'మంచుకు సున్నితమైన పంటలను రక్షించండి, నాటడం ఆలస్యం చేయండి'
            }
        }
        
        lang_impacts = impacts.get(lang, impacts['en'])
        
        for key, impact in lang_impacts.items():
            if key in event:
                return impact
        
        return 'Monitor weather conditions closely' if lang == 'en' else 'मौसम की स्थिति की बारीकी से निगरानी करें' if lang == 'hi' else 'వాతావరణ పరిస్థితులను నిశితంగా పర్యవేక్షించండి'


# Initialize weather service
weather_service = WeatherService()
