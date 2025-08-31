from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random

from core.models import UserProfile, FAQ, ContactMessage, AppSettings
from weather.models import WeatherData, WeatherForecast, WeatherAlert
from crops.models import Crop, CropSchedule, CropDisease, CropPest
from marketplace.models import Vendor, ProductCategory, Product
from community.models import ForumCategory, ForumTopic, Expert, Question
from schemes.models import GovernmentScheme
from soil_health.models import SoilType, SoilTip, Fertilizer


class Command(BaseCommand):
            help = 'Populate the database with sample data for Farmazee'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample users
        self.create_sample_users()
        
        # Create sample weather data
        self.create_sample_weather_data()
        
        # Create sample crops
        self.create_sample_crops()
        
        # Create sample marketplace data
        self.create_sample_marketplace_data()
        
        # Create sample community data
        self.create_sample_community_data()
        
        # Create sample government schemes
        self.create_sample_schemes()
        
        # Create sample soil health data
        self.create_sample_soil_health_data()
        
        # Create sample FAQs
        self.create_sample_faqs()
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))

    def create_sample_users(self):
        """Create sample users and profiles"""
        users_data = [
            {'username': 'farmer1', 'email': 'farmer1@example.com', 'first_name': 'Ramesh', 'last_name': 'Kumar'},
            {'username': 'farmer2', 'email': 'farmer2@example.com', 'first_name': 'Sita', 'last_name': 'Devi'},
            {'username': 'expert1', 'email': 'expert1@example.com', 'first_name': 'Dr. Rajesh', 'last_name': 'Singh'},
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                
                # Create user profile
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'phone_number': f'+91{random.randint(9000000000, 9999999999)}',
                        'address': f'Farm {random.randint(1, 100)}, Village {random.randint(1, 50)}',
                        'land_area': random.randint(1, 50),
                        'village': f'Village {random.randint(1, 50)}',
                        'district': 'Hyderabad',
                        'state': 'Telangana',
                    }
                )

    def create_sample_weather_data(self):
        """Create sample weather data"""
        # Current weather
        WeatherData.objects.get_or_create(
            location='Hyderabad',
            defaults={
                'temperature': 28.5,
                'humidity': 65,
                'wind_speed': 12.0,
                'description': 'Partly Cloudy',
                'pressure': 1013.25,
                'visibility': 10.0,
                'is_current': True,
            }
        )
        
        # Weather forecast
        for i in range(5):
            WeatherForecast.objects.get_or_create(
                date=timezone.now().date() + timedelta(days=i+1),
                location='Hyderabad',
                defaults={
                    'max_temperature': random.randint(25, 35),
                    'min_temperature': random.randint(15, 25),
                    'description': random.choice(['Clear', 'Cloudy', 'Rain', 'Partly Cloudy']),
                    'humidity': random.randint(50, 80),
                    'wind_speed': random.uniform(5.0, 15.0),
                }
            )
        
        # Weather alerts
        WeatherAlert.objects.get_or_create(
            title='Heavy Rain Alert',
            defaults={
                'description': 'Heavy rainfall expected in the next 24 hours',
                'severity': 'medium',
                'location': 'Hyderabad',
                'alert_type': 'rain',
                'start_time': timezone.now(),
                'end_time': timezone.now() + timedelta(days=1),
            }
        )

    def create_sample_crops(self):
        """Create sample crops"""
        crops_data = [
            {
                'name': 'Rice',
                'description': 'Staple food crop grown in paddy fields',
                'category': 'cereals',
                'season': 'kharif',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'rainfall_requirement': 'High rainfall (1000-2000mm)',
                'soil_type': 'Clay loam',
                'ph_range': '6.0-7.0',
                'sowing_time': 'June-July',
                'harvesting_time': 'October-November',
                'growth_duration': '120-150 days',
                'yield_per_acre': '25-30 quintals',
                'watering_needs': 'Requires standing water during initial growth',
                'fertilizer_needs': 'NPK 120:60:60 kg/ha',
                'pest_management': 'Use neem oil and biological control',
                'disease_management': 'Treat seeds with fungicide',
                'market_price_range': '₹1500-2000 per quintal',
                'demand_level': 'high',
            },
            {
                'name': 'Wheat',
                'description': 'Winter cereal crop',
                'category': 'cereals',
                'season': 'rabi',
                'min_temperature': 15.0,
                'max_temperature': 25.0,
                'rainfall_requirement': 'Moderate rainfall (400-600mm)',
                'soil_type': 'Loamy soil',
                'ph_range': '6.5-7.5',
                'sowing_time': 'November-December',
                'harvesting_time': 'March-April',
                'growth_duration': '140-160 days',
                'yield_per_acre': '20-25 quintals',
                'watering_needs': 'Requires 4-5 irrigations',
                'fertilizer_needs': 'NPK 120:60:40 kg/ha',
                'pest_management': 'Monitor for aphids and termites',
                'disease_management': 'Use disease-resistant varieties',
                'market_price_range': '₹1800-2200 per quintal',
                'demand_level': 'high',
            },
            {
                'name': 'Tomato',
                'description': 'Popular vegetable crop',
                'category': 'vegetables',
                'season': 'zaid',
                'min_temperature': 20.0,
                'max_temperature': 30.0,
                'rainfall_requirement': 'Moderate rainfall (600-800mm)',
                'soil_type': 'Sandy loam',
                'ph_range': '6.0-7.0',
                'sowing_time': 'February-March',
                'harvesting_time': 'May-June',
                'growth_duration': '90-120 days',
                'yield_per_acre': '15-20 tons',
                'watering_needs': 'Regular irrigation needed',
                'fertilizer_needs': 'NPK 100:50:50 kg/ha',
                'pest_management': 'Use integrated pest management',
                'disease_management': 'Control early blight and late blight',
                'market_price_range': '₹20-40 per kg',
                'demand_level': 'high',
            },
        ]
        
        for crop_data in crops_data:
            Crop.objects.get_or_create(
                name=crop_data['name'],
                defaults=crop_data
            )

    def create_sample_marketplace_data(self):
        """Create sample marketplace data"""
        # Create vendors
        vendors_data = [
            {
                'business_name': 'Agri Supply Co.',
                'business_description': 'Leading agricultural supplies',
                'phone_number': '+919876543210',
                'address': '123 Agri Street, Hyderabad',
                'city': 'Hyderabad',
                'state': 'Telangana',
                'pincode': '500001',
            },
            {
                'business_name': 'Farm Tools Ltd.',
                'business_description': 'Quality farming tools and equipment',
                'phone_number': '+919876543211',
                'address': '456 Farm Road, Hyderabad',
                'city': 'Hyderabad',
                'state': 'Telangana',
                'pincode': '500002',
            },
        ]
        
        for vendor_data in vendors_data:
            # Create a user for the vendor
            user, created = User.objects.get_or_create(
                username=f"vendor_{vendor_data['business_name'].lower().replace(' ', '_')}",
                defaults={
                    'email': f"{vendor_data['business_name'].lower().replace(' ', '_')}@example.com",
                    'first_name': vendor_data['business_name'].split()[0],
                    'last_name': vendor_data['business_name'].split()[-1],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            
            vendor, created = Vendor.objects.get_or_create(
                user=user,
                defaults=vendor_data
            )
            
            if created:
                # Create products for this vendor
                products_data = [
                    {
                        'name': 'Organic Seeds Pack',
                        'description': 'High-quality organic seeds',
                        'price': 150.00,
                        'category': ProductCategory.objects.get_or_create(name='Seeds')[0],
                    },
                    {
                        'name': 'Fertilizer Mix',
                        'description': 'Balanced NPK fertilizer',
                        'price': 500.00,
                        'category': ProductCategory.objects.get_or_create(name='Fertilizers')[0],
                    },
                ]
                
                for product_data in products_data:
                    Product.objects.get_or_create(
                        name=product_data['name'],
                        vendor=vendor,
                        defaults=product_data
                    )

    def create_sample_community_data(self):
        """Create sample community data"""
        # Create forum categories
        categories_data = [
            {'name': 'General Farming', 'description': 'General farming discussions'},
            {'name': 'Crop Management', 'description': 'Crop-specific discussions'},
        ]
        
        for cat_data in categories_data:
            category, created = ForumCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            
            if created:
                # Create topics for this category
                topics_data = [
                    {
                        'title': 'Best practices for organic farming',
                        'content': 'Share your experiences with organic farming methods',
                        'author': User.objects.first(),
                    },
                    {
                        'title': 'Water management techniques',
                        'content': 'Discuss efficient water management in agriculture',
                        'author': User.objects.first(),
                    },
                ]
                
                for topic_data in topics_data:
                    ForumTopic.objects.get_or_create(
                        title=topic_data['title'],
                        category=category,
                        defaults=topic_data
                    )

    def create_sample_schemes(self):
        """Create sample government schemes"""
        schemes_data = [
            {
                'title': 'PM-KISAN',
                'description': 'Direct income support for farmers',
                'category': 'subsidy',
                'scheme_amount': '₹6,000 per year',
                'deadline': timezone.now().date() + timedelta(days=30),
                'eligibility_criteria': 'Small and marginal farmers with landholding up to 2 hectares',
                'benefits': 'Direct cash transfer of ₹6,000 per year in three equal installments',
                'application_process': 'Apply through PM-KISAN portal or visit nearest agriculture office',
                'required_documents': 'Aadhaar card, land records, bank account details',
                'contact_information': 'PM-KISAN Helpline: 1800-180-1551',
                'states': 'All India',
                'is_active': True,
            },
            {
                'title': 'Kisan Credit Card',
                'description': 'Easy credit for agricultural needs',
                'category': 'loan',
                'scheme_amount': 'Up to ₹5,00,000',
                'deadline': timezone.now().date() + timedelta(days=60),
                'eligibility_criteria': 'Farmers with landholding and good credit history',
                'benefits': 'Easy credit access with low interest rates',
                'application_process': 'Apply through your bank or cooperative society',
                'required_documents': 'Land documents, income certificate, bank statements',
                'contact_information': 'Contact your nearest bank branch',
                'states': 'All India',
                'is_active': True,
            },
        ]
        
        for scheme_data in schemes_data:
            GovernmentScheme.objects.get_or_create(
                title=scheme_data['title'],
                defaults=scheme_data
            )

    def create_sample_soil_health_data(self):
        """Create sample soil health data"""
        # Create soil types
        soil_types_data = [
            {'name': 'Clay Soil', 'description': 'Heavy soil with high water retention'},
            {'name': 'Sandy Soil', 'description': 'Light soil with good drainage'},
            {'name': 'Loamy Soil', 'description': 'Balanced soil ideal for most crops'},
        ]
        
        for soil_data in soil_types_data:
            SoilType.objects.get_or_create(
                name=soil_data['name'],
                defaults=soil_data
            )
        
        # Create soil tips
        tips_data = [
            {
                'title': 'Improving Soil Fertility',
                'content': 'Add organic matter like compost to improve soil fertility',
                'category': 'fertility',
            },
            {
                'title': 'Soil Testing',
                'content': 'Regular soil testing helps determine nutrient requirements',
                'category': 'testing',
            },
        ]
        
        for tip_data in tips_data:
            SoilTip.objects.get_or_create(
                title=tip_data['title'],
                defaults=tip_data
            )

    def create_sample_faqs(self):
        """Create sample FAQs"""
        faqs_data = [
            {
                'question': 'How do I register for government schemes?',
                'answer': 'You can register through the official portal or visit your nearest agriculture office.',
                'category': 'schemes',
            },
            {
                'question': 'What is the best time to plant rice?',
                'answer': 'Rice is typically planted during the monsoon season (June-July) for kharif crop.',
                'category': 'crops',
            },
        ]
        
        for faq_data in faqs_data:
            FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
