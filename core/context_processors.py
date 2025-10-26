from .models import SystemSettings
from django.utils import timezone
from datetime import timedelta


def system_settings(request):
    """Add system settings to template context"""
    try:
        settings = SystemSettings.get_settings()
        context = {
            'system_settings': settings,
            'site_name': settings.site_name,
            'site_description': settings.site_description,
            'maintenance_mode': settings.maintenance_mode,
            'maintenance_message': settings.maintenance_message,
            'primary_color': settings.primary_color,
            'secondary_color': settings.secondary_color,
            'accent_color': settings.accent_color,
            'font_family': settings.font_family,
            'enable_dark_mode': settings.enable_dark_mode,
            'default_theme': settings.default_theme,
            'homepage_title': settings.homepage_title,
            'homepage_subtitle': settings.homepage_subtitle,
            'footer_text': settings.footer_text,
            'enable_marketplace': settings.enable_marketplace,
            'enable_community': settings.enable_community,
            'enable_ai_chatbot': settings.enable_ai_chatbot,
            'enable_weather': settings.enable_weather,
            'enable_soil_health': settings.enable_soil_health,
            'enable_crop_planning': settings.enable_crop_planning,
            'enable_schemes': settings.enable_schemes,
            'meta_title': settings.meta_title,
            'meta_description': settings.meta_description,
            'meta_keywords': settings.meta_keywords,
            'google_analytics_id': settings.google_analytics_id,
            'facebook_pixel_id': settings.facebook_pixel_id,
            'facebook_url': settings.facebook_url,
            'twitter_url': settings.twitter_url,
            'instagram_url': settings.instagram_url,
            'youtube_url': settings.youtube_url,
            'linkedin_url': settings.linkedin_url,
        }
        # Disease indicator removed per request
        context['disease_alert'] = False
        return context
    except Exception:
        # Return default values if settings are not available
        context = {
            'system_settings': None,
            'site_name': 'Farmazee',
            'site_description': 'Smart Farming Solutions',
            'maintenance_mode': False,
            'maintenance_message': 'Site is under maintenance. Please check back later.',
            'primary_color': '#007bff',
            'secondary_color': '#6c757d',
            'accent_color': '#28a745',
            'font_family': 'Inter, sans-serif',
            'enable_dark_mode': False,
            'default_theme': 'light',
            'homepage_title': 'Welcome to Farmazee',
            'homepage_subtitle': 'Your smart farming companion',
            'footer_text': '© 2024 Farmazee. All rights reserved.',
            'enable_marketplace': True,
            'enable_community': True,
            'enable_ai_chatbot': True,
            'enable_weather': True,
            'enable_soil_health': True,
            'enable_crop_planning': True,
            'enable_schemes': True,
            'meta_title': 'Farmazee - Smart Farming Solutions',
            'meta_description': 'Farmazee provides smart farming solutions, crop advice, and agricultural tools for modern farmers.',
            'meta_keywords': 'farming, agriculture, crop planning, soil health, smart farming',
            'google_analytics_id': '',
            'facebook_pixel_id': '',
            'facebook_url': '',
            'twitter_url': '',
            'instagram_url': '',
            'youtube_url': '',
            'linkedin_url': '',
        }
        context['disease_alert'] = False
        return context
