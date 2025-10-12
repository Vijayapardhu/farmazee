from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
import random


class Command(BaseCommand):
    help = 'Populate the database with comprehensive sample data'

    def handle(self, *args, **options):
        self.stdout.write('Populating sample data...')
        
        # Populate in order of dependencies
        self.create_users()
        self.create_user_profiles()
        self.create_crops()
        self.create_marketplace_data()
        self.create_government_schemes()
        self.create_community_data()
        self.create_farmer_problems()
        self.create_soil_health_data()
        self.create_ai_knowledge_base()
        self.create_weather_data()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated comprehensive sample data!')
        )

    def create_users(self):
        """Create sample users"""
        self.stdout.write('Creating users...')
        
        users_data = [
            {'username': 'farmer1', 'email': 'farmer1@farmazee.com', 'first_name': 'Rajesh', 'last_name': 'Kumar'},
            {'username': 'farmer2', 'email': 'farmer2@farmazee.com', 'first_name': 'Priya', 'last_name': 'Sharma'},
            {'username': 'farmer3', 'email': 'farmer3@farmazee.com', 'first_name': 'Amit', 'last_name': 'Singh'},
            {'username': 'expert1', 'email': 'expert1@farmazee.com', 'first_name': 'Dr. Suresh', 'last_name': 'Patel'},
            {'username': 'expert2', 'email': 'expert2@farmazee.com', 'first_name': 'Dr. Meera', 'last_name': 'Reddy'},
            {'username': 'admin_user', 'email': 'admin@farmazee.com', 'first_name': 'Admin', 'last_name': 'User'},
        ]
        
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'is_active': True,
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')

    def create_user_profiles(self):
        """Create user profiles"""
        self.stdout.write('Creating user profiles...')
        
        try:
            from core.models import UserProfile
            
            profiles_data = [
                {'username': 'farmer1', 'village': 'Hyderabad', 'phone_number': '9876543210', 'farm_type': 'small', 'experience_years': 'intermediate'},
                {'username': 'farmer2', 'village': 'Delhi', 'phone_number': '9876543211', 'farm_type': 'medium', 'experience_years': 'experienced'},
                {'username': 'farmer3', 'village': 'Mumbai', 'phone_number': '9876543212', 'farm_type': 'large', 'experience_years': 'expert'},
                {'username': 'expert1', 'village': 'Bangalore', 'phone_number': '9876543213', 'farm_type': 'organic', 'experience_years': 'expert'},
                {'username': 'expert2', 'village': 'Chennai', 'phone_number': '9876543214', 'farm_type': 'commercial', 'experience_years': 'expert'},
                {'username': 'admin_user', 'village': 'Pune', 'phone_number': '9876543215', 'farm_type': 'small', 'experience_years': 'beginner'},
            ]
            
            for profile_data in profiles_data:
                try:
                    user = User.objects.get(username=profile_data['username'])
                    profile, created = UserProfile.objects.get_or_create(
                        user=user,
                        defaults={
                            'village': profile_data['village'],
                            'phone_number': profile_data['phone_number'],
                            'farm_type': profile_data['farm_type'],
                            'experience_years': profile_data['experience_years'],
                            'address': f"Sample address in {profile_data['village']}",
                            'district': profile_data['village'],
                            'state': 'Telangana' if 'Hyderabad' in profile_data['village'] else 'Maharashtra',
                        }
                    )
                    if created:
                        self.stdout.write(f'Created profile for: {user.username}')
                except User.DoesNotExist:
                    self.stdout.write(f'User not found: {profile_data["username"]}')
                    
        except ImportError:
            self.stdout.write('UserProfile model not found, skipping...')

    def create_crops(self):
        """Create sample crops"""
        self.stdout.write('Creating crops...')
        
        try:
            from crops.models import Crop
            
            crops_data = [
                {
                    'name': 'Rice',
                    'scientific_name': 'Oryza sativa',
                    'description': 'Staple food crop grown in flooded fields. Essential for food security in India.',
                    'category': 'cereals',
                    'season': 'kharif',
                    'min_temperature': 20.0,
                    'max_temperature': 35.0,
                    'rainfall_requirement': '1000-2000 mm',
                    'soil_type': 'Clay loam',
                    'ph_range': '6.0-7.5',
                    'sowing_time': 'June-July (with onset of monsoon)',
                    'harvesting_time': 'October-November',
                    'growth_duration': '120-150 days',
                    'yield_per_acre': '25-30 quintals',
                    'watering_needs': 'Flood irrigation, maintain 5-10 cm water depth',
                    'sunlight_requirements': 'Full sun, 8-10 hours daily',
                    'care_instructions': 'Regular weeding, proper water management, pest control',
                    'harvesting_tips': 'Harvest when 80% of grains are mature and moisture content is 20-25%',
                    'is_active': True
                },
                {
                    'name': 'Wheat',
                    'scientific_name': 'Triticum aestivum',
                    'description': 'Winter cereal crop providing essential carbohydrates and protein.',
                    'category': 'cereals',
                    'season': 'rabi',
                    'min_temperature': 15.0,
                    'max_temperature': 25.0,
                    'rainfall_requirement': '500-800 mm',
                    'soil_type': 'Well-drained loamy soil',
                    'ph_range': '6.5-7.5',
                    'sowing_time': 'October-November',
                    'harvesting_time': 'March-April',
                    'growth_duration': '120-140 days',
                    'yield_per_acre': '20-25 quintals',
                    'watering_needs': '3-4 irrigations at critical growth stages',
                    'sunlight_requirements': 'Full sun, 6-8 hours daily',
                    'care_instructions': 'Proper seed rate, timely weeding, disease management',
                    'harvesting_tips': 'Harvest when grains are hard and moisture content is 12-14%',
                    'is_active': True
                },
                {
                    'name': 'Tomato',
                    'scientific_name': 'Solanum lycopersicum',
                    'description': 'Popular vegetable crop rich in vitamins and antioxidants.',
                    'category': 'vegetables',
                    'season': 'all_season',
                    'min_temperature': 20.0,
                    'max_temperature': 30.0,
                    'rainfall_requirement': '600-800 mm',
                    'soil_type': 'Well-drained sandy loam',
                    'ph_range': '6.0-7.0',
                    'sowing_time': 'Year-round with proper protection',
                    'harvesting_time': 'Continuous harvesting',
                    'growth_duration': '90-120 days',
                    'yield_per_acre': '200-300 quintals',
                    'watering_needs': 'Regular watering, avoid water stress',
                    'sunlight_requirements': 'Full sun, 6-8 hours daily',
                    'care_instructions': 'Staking, pruning, pest and disease control',
                    'harvesting_tips': 'Harvest when fruits are fully colored but firm',
                    'is_active': True
                },
                {
                    'name': 'Cotton',
                    'scientific_name': 'Gossypium hirsutum',
                    'description': 'Cash crop for fiber and oil production.',
                    'category': 'cash_crops',
                    'season': 'kharif',
                    'min_temperature': 25.0,
                    'max_temperature': 35.0,
                    'rainfall_requirement': '600-1000 mm',
                    'soil_type': 'Black cotton soil',
                    'ph_range': '6.0-8.0',
                    'sowing_time': 'April-May',
                    'harvesting_time': 'October-December',
                    'growth_duration': '150-180 days',
                    'yield_per_acre': '15-20 quintals',
                    'watering_needs': 'Critical irrigation at flowering and boll formation',
                    'sunlight_requirements': 'Full sun, 8-10 hours daily',
                    'care_instructions': 'Proper spacing, pest management, boll opening',
                    'harvesting_tips': 'Harvest when bolls are fully opened and dry',
                    'is_active': True
                }
            ]
            
            for crop_data in crops_data:
                crop, created = Crop.objects.get_or_create(
                    name=crop_data['name'],
                    defaults=crop_data
                )
                if created:
                    self.stdout.write(f'Created crop: {crop.name}')
                    
        except ImportError:
            self.stdout.write('Crop model not found, skipping...')

    def create_marketplace_data(self):
        """Create marketplace data"""
        self.stdout.write('Creating marketplace data...')
        
        try:
            from marketplace.models import Product, ProductCategory
            
            # Create categories
            categories_data = [
                {'name': 'Seeds', 'description': 'High-quality seeds for various crops'},
                {'name': 'Fertilizers', 'description': 'Organic and chemical fertilizers'},
                {'name': 'Pesticides', 'description': 'Crop protection chemicals'},
                {'name': 'Tools', 'description': 'Farming tools and equipment'},
                {'name': 'Machinery', 'description': 'Agricultural machinery'},
                {'name': 'Irrigation', 'description': 'Irrigation systems and accessories'},
            ]
            
            categories = {}
            for cat_data in categories_data:
                category, created = ProductCategory.objects.get_or_create(
                    name=cat_data['name'],
                    defaults=cat_data
                )
                categories[cat_data['name']] = category
                if created:
                    self.stdout.write(f'Created category: {category.name}')
            
            # Create a vendor first
            vendor_user = User.objects.filter(username='farmer1').first()
            if vendor_user:
                from marketplace.models import Vendor
                vendor, created = Vendor.objects.get_or_create(
                    user=vendor_user,
                    defaults={
                        'business_name': 'AgriCorp Solutions',
                        'business_description': 'Leading agricultural input supplier',
                        'phone_number': '9876543210',
                        'address': 'Agricultural Market, Hyderabad',
                        'city': 'Hyderabad',
                        'state': 'Telangana',
                        'pincode': '500001',
                        'is_verified': True,
                        'is_active': True
                    }
                )
                
                # Create products
                products_data = [
                    {
                        'vendor': vendor,
                        'name': 'Hybrid Rice Seeds - BPT-5204',
                        'description': 'High-yielding hybrid rice seeds with disease resistance and 120-day maturity. Suitable for all soil types.',
                        'short_description': 'High-yielding hybrid rice seeds with disease resistance',
                        'category': categories['Seeds'],
                        'price': 250.00,
                        'unit': 'kg',
                        'stock_quantity': 1000,
                        'brand': 'AgriCorp',
                        'is_active': True,
                        'is_certified': True
                    },
                    {
                        'vendor': vendor,
                        'name': 'NPK Fertilizer 19:19:19',
                        'description': 'Balanced NPK fertilizer for all crops with fast absorption. Water soluble formulation.',
                        'short_description': 'Balanced NPK fertilizer for all crops',
                        'category': categories['Fertilizers'],
                        'price': 45.00,
                        'unit': 'kg',
                        'stock_quantity': 5000,
                        'brand': 'GreenFarm',
                        'is_active': True,
                        'is_certified': True
                    },
                    {
                        'vendor': vendor,
                        'name': 'Neem Oil Pesticide',
                        'description': 'Organic pest control solution safe for beneficial insects. 100% natural and eco-friendly.',
                        'short_description': 'Organic pest control solution',
                        'category': categories['Pesticides'],
                        'price': 180.00,
                        'unit': 'liter',
                        'stock_quantity': 200,
                        'brand': 'Organic Solutions',
                        'is_active': True,
                        'is_organic': True
                    },
                    {
                        'vendor': vendor,
                        'name': 'Hand Hoe - Premium Grade',
                        'description': 'Traditional hand tool for weeding and cultivation with durable steel construction.',
                        'short_description': 'Premium hand tool for weeding and cultivation',
                        'category': categories['Tools'],
                        'price': 350.00,
                        'unit': 'piece',
                        'stock_quantity': 100,
                        'brand': 'Farm Tools Co',
                        'is_active': True
                    }
                ]
                
                for product_data in products_data:
                    product, created = Product.objects.get_or_create(
                        name=product_data['name'],
                        defaults=product_data
                    )
                    if created:
                        self.stdout.write(f'Created product: {product.name}')
                    
        except ImportError:
            self.stdout.write('Marketplace models not found, skipping...')

    def create_government_schemes(self):
        """Create government schemes"""
        self.stdout.write('Creating government schemes...')
        
        try:
            from schemes.models import GovernmentScheme
            
            schemes_data = [
                {
                    'title': 'PM Kisan Samman Nidhi',
                    'description': 'Direct income support scheme for farmers with ₹6000 per year in three installments. Provides financial assistance to small and marginal farmers.',
                    'category': 'subsidy',
                    'benefits': '₹6000 per year in three installments of ₹2000 each',
                    'eligibility_criteria': 'Small and marginal farmers with cultivable land up to 2 hectares',
                    'application_process': 'Online application through PM-KISAN portal or visit nearest CSC',
                    'required_documents': 'Aadhaar card, Bank account details, Land records, Income certificate',
                    'contact_information': 'PM-KISAN Helpline: 1800-180-1551, Email: pmkisan.gov.in',
                    'website_url': 'https://pmkisan.gov.in',
                    'helpline_number': '1800-180-1551',
                    'scheme_amount': '₹6000 per year',
                    'states': 'All states and union territories',
                    'is_active': True,
                    'is_featured': True
                },
                {
                    'title': 'Pradhan Mantri Fasal Bima Yojana',
                    'description': 'Crop insurance scheme for farmers with premium subsidy up to 90%. Protects farmers against crop losses.',
                    'category': 'insurance',
                    'benefits': 'Premium subsidy up to 90%, Comprehensive coverage against natural disasters',
                    'eligibility_criteria': 'All farmers growing notified crops in notified areas',
                    'application_process': 'Through Common Service Centers, online portal, or insurance companies',
                    'required_documents': 'Land records, Bank account, Crop details, Aadhaar card',
                    'contact_information': 'PMFBY Helpline: 1800-180-1551, Insurance company offices',
                    'website_url': 'https://pmfby.gov.in',
                    'helpline_number': '1800-180-1551',
                    'scheme_amount': 'Premium subsidy up to 90%',
                    'states': 'All states and union territories',
                    'is_active': True,
                    'is_featured': True
                },
                {
                    'title': 'Soil Health Card Scheme',
                    'description': 'Free soil testing and recommendations for all farmers to improve soil health and productivity.',
                    'category': 'technology',
                    'benefits': 'Free soil testing, Personalized recommendations, Improved crop yield',
                    'eligibility_criteria': 'All farmers with cultivable land',
                    'application_process': 'Apply at nearest soil testing lab or online through portal',
                    'required_documents': 'Aadhaar card, Land records, Application form',
                    'contact_information': 'Soil Health Card Portal, State agriculture department',
                    'website_url': 'https://soilhealth.dac.gov.in',
                    'helpline_number': '1800-180-1551',
                    'states': 'All states and union territories',
                    'is_active': True
                }
            ]
            
            for scheme_data in schemes_data:
                scheme, created = GovernmentScheme.objects.get_or_create(
                    title=scheme_data['title'],
                    defaults=scheme_data
                )
                if created:
                    self.stdout.write(f'Created scheme: {scheme.title}')
                    
        except ImportError:
            self.stdout.write('GovernmentScheme model not found, skipping...')

    def create_community_data(self):
        """Create community discussions"""
        self.stdout.write('Creating community data...')
        
        try:
            from community.models import Topic, Discussion
            
            # Create topics
            topics_data = [
                {'title': 'Organic Farming', 'description': 'Discuss organic farming methods and benefits'},
                {'title': 'Crop Rotation', 'description': 'Share experiences with crop rotation techniques'},
                {'title': 'Water Management', 'description': 'Tips for efficient water usage in agriculture'},
                {'title': 'Pest Control', 'description': 'Natural and chemical pest control methods'},
                {'title': 'Market Prices', 'description': 'Share and discuss current market prices'},
                {'title': 'Soil Health', 'description': 'Soil testing, improvement, and fertility management'},
                {'title': 'Weather Impact', 'description': 'Discuss weather effects on farming'},
                {'title': 'Government Schemes', 'description': 'Information about government schemes and benefits'},
            ]
            
            topics = {}
            for topic_data in topics_data:
                topic, created = Topic.objects.get_or_create(
                    title=topic_data['title'],
                    defaults=topic_data
                )
                topics[topic_data['title']] = topic
                if created:
                    self.stdout.write(f'Created topic: {topic.title}')
            
            # Create discussions
            discussions_data = [
                {
                    'topic': topics['Organic Farming'],
                    'title': 'Best Organic Fertilizers for Rice',
                    'content': 'I have been using organic fertilizers for my rice crop. Compost and vermicompost have given excellent results. What are your experiences with organic farming?',
                    'author': User.objects.get(username='farmer1')
                },
                {
                    'topic': topics['Water Management'],
                    'title': 'Drip Irrigation Setup Cost',
                    'content': 'Planning to install drip irrigation for my 2-acre farm. Can anyone share the cost breakdown and benefits they have experienced?',
                    'author': User.objects.get(username='farmer2')
                },
                {
                    'topic': topics['Pest Control'],
                    'title': 'Natural Pest Control Methods',
                    'content': 'Looking for eco-friendly ways to control aphids in my tomato crop. Neem oil seems to work but any other suggestions?',
                    'author': User.objects.get(username='farmer3')
                },
                {
                    'topic': topics['Market Prices'],
                    'title': 'Current Rice Prices in Telangana',
                    'content': 'What are the current rice prices in different mandis of Telangana? Planning to sell my harvest next week.',
                    'author': User.objects.get(username='farmer1')
                },
                {
                    'topic': topics['Soil Health'],
                    'title': 'Soil pH Testing at Home',
                    'content': 'Can anyone guide me on how to test soil pH at home? I want to check my soil before planting next season.',
                    'author': User.objects.get(username='farmer2')
                }
            ]
            
            for discussion_data in discussions_data:
                discussion, created = Discussion.objects.get_or_create(
                    title=discussion_data['title'],
                    defaults=discussion_data
                )
                if created:
                    self.stdout.write(f'Created discussion: {discussion.title}')
                    
        except ImportError:
            self.stdout.write('Community models not found, skipping...')

    def create_farmer_problems(self):
        """Create farmer problems and solutions"""
        self.stdout.write('Creating farmer problems...')
        
        try:
            from farmer_problems.models import FarmerProblem, ProblemCategory, Solution, ExpertProfile
            
            # Create categories
            categories_data = [
                {'name': 'Pest Control', 'slug': 'pest-control', 'description': 'Issues related to pest management'},
                {'name': 'Disease Management', 'slug': 'disease-management', 'description': 'Crop diseases and treatments'},
                {'name': 'Soil Health', 'slug': 'soil-health', 'description': 'Soil-related problems'},
                {'name': 'Water Management', 'slug': 'water-management', 'description': 'Irrigation and water issues'},
                {'name': 'Fertilizer', 'slug': 'fertilizer', 'description': 'Fertilizer application and management'},
                {'name': 'Weather Impact', 'slug': 'weather-impact', 'description': 'Weather-related crop issues'},
                {'name': 'Harvesting', 'slug': 'harvesting', 'description': 'Harvest timing and techniques'},
                {'name': 'Storage', 'slug': 'storage', 'description': 'Crop storage and post-harvest management'},
            ]
            
            categories = {}
            for cat_data in categories_data:
                category, created = ProblemCategory.objects.get_or_create(
                    name=cat_data['name'],
                    defaults=cat_data
                )
                categories[cat_data['name']] = category
                if created:
                    self.stdout.write(f'Created problem category: {category.name}')
            
            # Create expert profiles
            experts = User.objects.filter(username__in=['expert1', 'expert2'])
            for expert in experts:
                profile, created = ExpertProfile.objects.get_or_create(
                    user=expert,
                    defaults={
                        'expert_type': 'agricultural_scientist',
                        'qualification': 'PhD in Agriculture',
                        'institution': 'Indian Agricultural Research Institute',
                        'years_of_experience': random.randint(5, 20),
                        'specialization': 'Crop Management and Soil Science',
                        'bio': f'Experienced agricultural expert with {random.randint(5, 20)} years in the field. Specializes in crop management and soil science.',
                        'is_verified': True
                    }
                )
                if created:
                    self.stdout.write(f'Created expert profile: {expert.username}')
            
            # Create problems
            problems_data = [
                {
                    'title': 'Yellow leaves on rice plants',
                    'slug': 'yellow-leaves-rice-plants',
                    'description': 'My rice plants are showing yellow leaves and stunted growth. The problem started about 2 weeks ago. I have been watering regularly and using NPK fertilizer.',
                    'category': categories['Disease Management'],
                    'author': User.objects.get(username='farmer1'),
                    'location': 'Hyderabad',
                    'crop_type': 'Rice'
                },
                {
                    'title': 'Aphids attacking tomato crop',
                    'slug': 'aphids-attacking-tomato-crop',
                    'description': 'Small green insects are damaging my tomato plants. They seem to multiply very fast and are causing the leaves to curl.',
                    'category': categories['Pest Control'],
                    'author': User.objects.get(username='farmer2'),
                    'location': 'Delhi',
                    'crop_type': 'Tomato'
                },
                {
                    'title': 'Poor soil fertility',
                    'slug': 'poor-soil-fertility',
                    'description': 'My soil has become less fertile over the years. Crop yields are declining despite using fertilizers. Need advice on soil improvement.',
                    'category': categories['Soil Health'],
                    'author': User.objects.get(username='farmer3'),
                    'location': 'Mumbai',
                    'crop_type': 'Wheat'
                },
                {
                    'title': 'Cotton bollworm infestation',
                    'slug': 'cotton-bollworm-infestation',
                    'description': 'Bollworms are damaging my cotton crop. I have tried some pesticides but they keep coming back. Need effective control measures.',
                    'category': categories['Pest Control'],
                    'author': User.objects.get(username='farmer1'),
                    'location': 'Hyderabad',
                    'crop_type': 'Cotton'
                },
                {
                    'title': 'Drip irrigation clogging',
                    'slug': 'drip-irrigation-clogging',
                    'description': 'My drip irrigation system keeps getting clogged. Water flow is irregular and some plants are not getting enough water.',
                    'category': categories['Water Management'],
                    'author': User.objects.get(username='farmer2'),
                    'location': 'Delhi',
                    'crop_type': 'Vegetables'
                }
            ]
            
            for problem_data in problems_data:
                problem, created = FarmerProblem.objects.get_or_create(
                    title=problem_data['title'],
                    defaults=problem_data
                )
                if created:
                    self.stdout.write(f'Created problem: {problem.title}')
                    
        except ImportError:
            self.stdout.write('Farmer problems models not found, skipping...')

    def create_soil_health_data(self):
        """Create soil health data"""
        self.stdout.write('Creating soil health data...')
        
        try:
            from soil_health.models import SoilTest, SoilTip
            
            # Create soil tips
            tips_data = [
                {
                    'title': 'Improve Soil Organic Matter',
                    'content': 'Add compost, manure, or green manure crops to increase organic matter content. This improves soil structure and water retention.',
                    'category': 'improvement'
                },
                {
                    'title': 'Test Soil pH Regularly',
                    'content': 'Most crops prefer pH between 6.0-7.5. Test your soil annually and adjust pH using lime or sulfur as needed.',
                    'category': 'testing'
                },
                {
                    'title': 'Practice Crop Rotation',
                    'content': 'Rotate crops to prevent nutrient depletion and reduce pest and disease buildup. Include legumes in rotation for nitrogen fixation.',
                    'category': 'conservation'
                },
                {
                    'title': 'Use Cover Crops',
                    'content': 'Plant cover crops during fallow periods to prevent erosion, suppress weeds, and add organic matter to soil.',
                    'category': 'erosion'
                },
                {
                    'title': 'Monitor Soil Moisture',
                    'content': 'Check soil moisture regularly. Overwatering can lead to nutrient leaching while underwatering stresses plants.',
                    'category': 'conservation'
                },
                {
                    'title': 'Add Beneficial Microorganisms',
                    'content': 'Use biofertilizers and mycorrhizal fungi to improve nutrient availability and plant health naturally.',
                    'category': 'organic'
                }
            ]
            
            for tip_data in tips_data:
                tip, created = SoilTip.objects.get_or_create(
                    title=tip_data['title'],
                    defaults=tip_data
                )
                if created:
                    self.stdout.write(f'Created soil tip: {tip.title}')
                    
        except ImportError:
            self.stdout.write('Soil health models not found, skipping...')

    def create_ai_knowledge_base(self):
        """Create AI knowledge base"""
        self.stdout.write('Creating AI knowledge base...')
        
        try:
            from ai_chatbot.models import KnowledgeBase
            
            knowledge_data = [
                {
                    'question': 'When is the best time to plant rice?',
                    'answer': 'Rice is typically planted during the Kharif season (June-July) when monsoon rains begin. The soil should be well-prepared and flooded.',
                    'category': 'Crop Planting',
                    'keywords': 'rice, planting, kharif, monsoon'
                },
                {
                    'question': 'How to control aphids naturally?',
                    'answer': 'Use neem oil spray (2ml per liter of water), introduce beneficial insects like ladybugs, or spray soap water solution. Avoid excessive nitrogen fertilization.',
                    'category': 'Pest Control',
                    'keywords': 'aphids, neem oil, natural control, ladybugs'
                },
                {
                    'question': 'What causes yellow leaves in plants?',
                    'answer': 'Yellow leaves can indicate nutrient deficiency (nitrogen, iron), overwatering, poor drainage, or disease. Check soil moisture and consider soil testing.',
                    'category': 'Plant Health',
                    'keywords': 'yellow leaves, nutrient deficiency, overwatering'
                },
                {
                    'question': 'How to improve soil fertility?',
                    'answer': 'Add organic matter (compost, manure), practice crop rotation, use cover crops, and maintain proper pH levels. Test soil regularly for nutrient content.',
                    'category': 'Soil Health',
                    'keywords': 'soil fertility, organic matter, crop rotation, pH'
                },
                {
                    'question': 'Best irrigation methods for vegetables?',
                    'answer': 'Drip irrigation is most efficient for vegetables. It saves water, reduces disease, and provides consistent moisture. Sprinkler irrigation works for leafy vegetables.',
                    'category': 'Irrigation',
                    'keywords': 'irrigation, drip, vegetables, water efficiency'
                },
                {
                    'question': 'How to prevent crop diseases?',
                    'answer': 'Practice crop rotation, use disease-resistant varieties, maintain proper spacing, avoid overhead watering, and remove infected plant debris promptly.',
                    'category': 'Disease Management',
                    'keywords': 'disease prevention, crop rotation, resistant varieties'
                },
                {
                    'question': 'When to harvest wheat?',
                    'answer': 'Harvest wheat when grains are hard and moisture content is 12-14%. This is usually 110-120 days after planting or when the crop turns golden yellow.',
                    'category': 'Harvesting',
                    'keywords': 'wheat, harvest, timing, moisture content'
                },
                {
                    'question': 'How to store harvested crops?',
                    'answer': 'Store in cool, dry, well-ventilated areas. Use proper containers, check for pests regularly, and maintain appropriate moisture levels for each crop type.',
                    'category': 'Storage',
                    'keywords': 'storage, harvest, moisture, pests'
                }
            ]
            
            for kb_data in knowledge_data:
                kb, created = KnowledgeBase.objects.get_or_create(
                    question=kb_data['question'],
                    defaults=kb_data
                )
                if created:
                    self.stdout.write(f'Created knowledge base entry: {kb.question[:50]}...')
                    
        except ImportError:
            self.stdout.write('AI knowledge base models not found, skipping...')

    def create_weather_data(self):
        """Create sample weather data"""
        self.stdout.write('Creating weather data...')
        
        try:
            from weather.models import WeatherData
            
            # Create sample weather data for different cities
            cities = ['Hyderabad', 'Delhi', 'Mumbai', 'Bangalore', 'Chennai']
            
            for city in cities:
                weather, created = WeatherData.objects.get_or_create(
                    location=city,
                    defaults={
                        'temperature': random.randint(20, 35),
                        'humidity': random.randint(40, 80),
                        'wind_speed': random.randint(5, 15),
                        'pressure': random.randint(1000, 1020),
                        'visibility': random.randint(5, 15),
                        'description': random.choice(['Clear', 'Partly Cloudy', 'Cloudy', 'Rainy']),
                        'is_current': True
                    }
                )
                if created:
                    self.stdout.write(f'Created weather data for: {city}')
                    
        except ImportError:
            self.stdout.write('Weather models not found, skipping...')