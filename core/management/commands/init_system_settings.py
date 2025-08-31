from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import SystemSettings


class Command(BaseCommand):
    help = 'Initialize default system settings'

    def handle(self, *args, **options):
        try:
            # Check if settings already exist
            if SystemSettings.objects.exists():
                self.stdout.write(
                    self.style.WARNING('System settings already exist. Skipping initialization.')
                )
                return

            # Create default settings
            settings = SystemSettings.objects.create(
                site_name='Farmazee',
                site_description='Smart Farming Solutions',
                timezone='Asia/Kolkata',
                language='en',
                maintenance_mode=False,
                maintenance_message='Site is under maintenance. Please check back later.',
                debug_mode=False,
                session_timeout=120,
                max_login_attempts=5,
                password_min_length=8,
                require_strong_password=True,
                enable_2fa=False,
                enable_csrf=True,
                allowed_hosts='*',
                smtp_host='smtp.gmail.com',
                smtp_port=587,
                smtp_username='',
                smtp_password='',
                from_email='noreply@farmazee.com',
                from_name='Farmazee',
                email_use_tls=True,
                email_use_ssl=False,
                email_notifications=True,
                sms_notifications=False,
                push_notifications=False,
                admin_alerts=True,
                notification_email='admin@farmazee.com',
                auto_backup=True,
                backup_frequency='daily',
                retain_backups=30,
                backup_location='/backups',
                last_backup=timezone.now(),
                openrouter_api_key='',
                weather_api_key='',
                google_maps_api_key='',
                payment_gateway='razorpay',
                primary_color='#007bff',
                secondary_color='#6c757d',
                accent_color='#28a745',
                font_family='Inter, sans-serif',
                enable_dark_mode=False,
                default_theme='light',
                homepage_title='Welcome to Farmazee',
                homepage_subtitle='Your smart farming companion',
                about_page_content='',
                contact_page_content='',
                footer_text='© 2024 Farmazee. All rights reserved.',
                enable_marketplace=True,
                enable_community=True,
                enable_ai_chatbot=True,
                enable_weather=True,
                enable_soil_health=True,
                enable_crop_planning=True,
                enable_schemes=True,
                meta_title='Farmazee - Smart Farming Solutions',
                meta_description='Farmazee provides smart farming solutions, crop advice, and agricultural tools for modern farmers.',
                meta_keywords='farming, agriculture, crop planning, soil health, smart farming',
                google_analytics_id='',
                facebook_pixel_id='',
                facebook_url='',
                twitter_url='',
                instagram_url='',
                youtube_url='',
                linkedin_url='',
                terms_of_service='',
                privacy_policy='',
                cookie_policy='',
                enable_caching=True,
                cache_timeout=300,
                enable_compression=True,
                enable_minification=True
            )

            self.stdout.write(
                self.style.SUCCESS(f'Successfully created system settings for {settings.site_name}')
            )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating system settings: {str(e)}')
            )
