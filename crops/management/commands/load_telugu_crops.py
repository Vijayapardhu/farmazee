from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from crops.models import (
    Crop, CropPlan, CropActivity, CropMonitoring, 
    PestDisease, CropCalendar, CropAdvice
)
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Load sample crop data for Telugu states (Telangana and Andhra Pradesh)'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample crop data for Telugu states...')
        
        # Create sample crops
        self.create_crops()
        
        # Create sample pest and diseases
        self.create_pest_diseases()
        
        # Create sample crop advice
        self.create_crop_advice()
        
        # Create sample crop calendar
        self.create_crop_calendar()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample crop data for Telugu states!')
        )

    def create_crops(self):
        """Create sample crops commonly grown in Telugu states"""
        
        crops_data = [
            # Cereals
            {
                'name': 'Rice (వరి)',
                'scientific_name': 'Oryza sativa',
                'category': 'cereals',
                'season': 'kharif',
                'description': 'Rice is the staple food crop of Telugu states. Telangana and Andhra Pradesh are major rice producers with extensive paddy cultivation.',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'rainfall_requirement': '1200-1500 mm',
                'soil_type': 'Clay loam, Alluvial soil',
                'ph_range': '6.0-7.0',
                'sowing_time': 'June-July (Kharif), January-February (Rabi)',
                'harvesting_time': 'October-November (Kharif), April-May (Rabi)',
                'growth_duration': '120-150 days',
                'yield_per_acre': '25-35 quintals',
                'watering_needs': 'Requires standing water for most of the growth period. Maintain 2-3 inches water level.',
                'sunlight_requirements': 'Full sunlight, 6-8 hours daily',
                'care_instructions': 'Regular weeding, proper water management, balanced fertilization with NPK.',
                'harvesting_tips': 'Harvest when 80% of grains are mature. Cut at ground level and thresh properly.',
                'is_featured': True,
            },
            {
                'name': 'Maize (మొక్కజొన్న)',
                'scientific_name': 'Zea mays',
                'category': 'cereals',
                'season': 'kharif',
                'description': 'Maize is an important cereal crop grown extensively in Telugu states for both food and fodder purposes.',
                'min_temperature': 18.0,
                'max_temperature': 32.0,
                'rainfall_requirement': '800-1000 mm',
                'soil_type': 'Well-drained loamy soil',
                'ph_range': '6.0-7.5',
                'sowing_time': 'June-July',
                'harvesting_time': 'September-October',
                'growth_duration': '90-120 days',
                'yield_per_acre': '20-30 quintals',
                'watering_needs': 'Regular irrigation, avoid waterlogging. Critical stages: knee-high, tasseling, silking.',
                'sunlight_requirements': 'Full sunlight',
                'care_instructions': 'Thinning, weeding, earthing up, balanced fertilization.',
                'harvesting_tips': 'Harvest when kernels are hard and moisture content is 20-25%.',
                'is_featured': True,
            },
            {
                'name': 'Jowar (జొన్న)',
                'scientific_name': 'Sorghum bicolor',
                'category': 'cereals',
                'season': 'kharif',
                'description': 'Jowar is a drought-resistant cereal crop well-suited for rainfed conditions in Telugu states.',
                'min_temperature': 15.0,
                'max_temperature': 35.0,
                'rainfall_requirement': '400-600 mm',
                'soil_type': 'Medium to heavy soils',
                'ph_range': '6.5-8.5',
                'sowing_time': 'June-July',
                'harvesting_time': 'October-November',
                'growth_duration': '90-120 days',
                'yield_per_acre': '15-25 quintals',
                'watering_needs': 'Drought-tolerant, but responds well to irrigation at critical stages.',
                'sunlight_requirements': 'Full sunlight',
                'care_instructions': 'Thinning, weeding, earthing up, bird scaring during grain formation.',
                'harvesting_tips': 'Harvest when grains are hard and moisture content is 20-25%.',
                'is_featured': False,
            },
            
            # Pulses
            {
                'name': 'Red Gram (కంది పప్పు)',
                'scientific_name': 'Cajanus cajan',
                'category': 'pulses',
                'season': 'kharif',
                'description': 'Red gram or pigeon pea is a major pulse crop in Telugu states, providing protein-rich food.',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'rainfall_requirement': '600-800 mm',
                'soil_type': 'Well-drained sandy loam to clay loam',
                'ph_range': '6.5-7.5',
                'sowing_time': 'June-July',
                'harvesting_time': 'December-January',
                'growth_duration': '150-180 days',
                'yield_per_acre': '8-12 quintals',
                'watering_needs': 'Drought-tolerant, but irrigation at flowering and pod formation increases yield.',
                'sunlight_requirements': 'Full sunlight',
                'care_instructions': 'Weeding, earthing up, protection from pod borer.',
                'harvesting_tips': 'Harvest when 80% pods are mature and dry.',
                'is_featured': True,
            },
            {
                'name': 'Green Gram (పెసర పప్పు)',
                'scientific_name': 'Vigna radiata',
                'category': 'pulses',
                'season': 'kharif',
                'description': 'Green gram is a short-duration pulse crop suitable for multiple cropping systems.',
                'min_temperature': 25.0,
                'max_temperature': 35.0,
                'rainfall_requirement': '400-600 mm',
                'soil_type': 'Well-drained sandy loam',
                'ph_range': '6.5-7.5',
                'sowing_time': 'June-July',
                'harvesting_time': 'September-October',
                'growth_duration': '60-90 days',
                'yield_per_acre': '6-10 quintals',
                'watering_needs': 'Light irrigation at critical stages, avoid waterlogging.',
                'sunlight_requirements': 'Full sunlight',
                'care_instructions': 'Weeding, protection from pod borer and yellow mosaic virus.',
                'harvesting_tips': 'Harvest when pods are dry and seeds are hard.',
                'is_featured': False,
            },
            
            # Oilseeds
            {
                'name': 'Groundnut (వేరుశనగ)',
                'scientific_name': 'Arachis hypogaea',
                'category': 'oilseeds',
                'season': 'kharif',
                'description': 'Groundnut is a major oilseed crop in Telugu states, providing both oil and protein.',
                'min_temperature': 25.0,
                'max_temperature': 35.0,
                'rainfall_requirement': '500-700 mm',
                'soil_type': 'Well-drained sandy loam',
                'ph_range': '6.0-7.0',
                'sowing_time': 'June-July',
                'harvesting_time': 'October-November',
                'growth_duration': '120-140 days',
                'yield_per_acre': '15-25 quintals',
                'watering_needs': 'Regular irrigation, critical at pegging and pod formation stages.',
                'sunlight_requirements': 'Full sunlight',
                'care_instructions': 'Earthing up, weeding, protection from leaf spot and rust diseases.',
                'harvesting_tips': 'Harvest when leaves turn yellow and pods are mature.',
                'is_featured': True,
            },
            {
                'name': 'Sunflower (పొద్దుతిరుగుడు)',
                'scientific_name': 'Helianthus annuus',
                'category': 'oilseeds',
                'season': 'rabi',
                'description': 'Sunflower is an important oilseed crop grown in rabi season in Telugu states.',
                'min_temperature': 15.0,
                'max_temperature': 30.0,
                'rainfall_requirement': '400-600 mm',
                'soil_type': 'Well-drained loamy soil',
                'ph_range': '6.0-7.5',
                'sowing_time': 'October-November',
                'harvesting_time': 'February-March',
                'growth_duration': '90-110 days',
                'yield_per_acre': '12-18 quintals',
                'watering_needs': 'Regular irrigation, critical at flowering and seed formation.',
                'sunlight_requirements': 'Full sunlight',
                'care_instructions': 'Thinning, weeding, protection from head borer.',
                'harvesting_tips': 'Harvest when back of head turns yellow and seeds are hard.',
                'is_featured': False,
            },
            
            # Vegetables
            {
                'name': 'Tomato (టమాట)',
                'scientific_name': 'Solanum lycopersicum',
                'category': 'vegetables',
                'season': 'all_season',
                'description': 'Tomato is a major vegetable crop grown throughout the year in Telugu states.',
                'min_temperature': 20.0,
                'max_temperature': 30.0,
                'rainfall_requirement': '600-800 mm',
                'soil_type': 'Well-drained sandy loam to clay loam',
                'ph_range': '6.0-7.0',
                'sowing_time': 'June-July, October-November, January-February',
                'harvesting_time': 'September-October, January-February, April-May',
                'growth_duration': '90-120 days',
                'yield_per_acre': '20-30 tonnes',
                'watering_needs': 'Regular irrigation, avoid waterlogging. Critical at flowering and fruit setting.',
                'sunlight_requirements': 'Full sunlight, 6-8 hours daily',
                'care_instructions': 'Staking, pruning, protection from early blight and fruit borer.',
                'harvesting_tips': 'Harvest at mature green or red ripe stage depending on market preference.',
                'is_featured': True,
            },
            {
                'name': 'Chilli (మిరప)',
                'scientific_name': 'Capsicum annuum',
                'category': 'vegetables',
                'season': 'kharif',
                'description': 'Chilli is a major spice crop and export commodity from Telugu states.',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'rainfall_requirement': '600-800 mm',
                'soil_type': 'Well-drained sandy loam to clay loam',
                'ph_range': '6.0-7.0',
                'sowing_time': 'June-July',
                'harvesting_time': 'October-December',
                'growth_duration': '120-150 days',
                'yield_per_acre': '15-25 quintals (dry)',
                'watering_needs': 'Regular irrigation, critical at flowering and fruit setting.',
                'sunlight_requirements': 'Full sunlight',
                'care_instructions': 'Staking, protection from thrips, mites, and viral diseases.',
                'harvesting_tips': 'Harvest at different stages: green, red ripe, and fully ripe for different purposes.',
                'is_featured': True,
            },
            
            # Fruits
            {
                'name': 'Mango (మామిడి)',
                'scientific_name': 'Mangifera indica',
                'category': 'fruits',
                'season': 'all_season',
                'description': 'Mango is the king of fruits and a major fruit crop in Telugu states.',
                'min_temperature': 15.0,
                'max_temperature': 40.0,
                'rainfall_requirement': '800-1200 mm',
                'soil_type': 'Deep, well-drained loamy soil',
                'ph_range': '6.0-7.5',
                'sowing_time': 'July-August (monsoon)',
                'harvesting_time': 'March-July (depending on variety)',
                'growth_duration': '4-6 years to first fruiting',
                'yield_per_acre': '8-15 tonnes (mature trees)',
                'watering_needs': 'Regular irrigation, critical at flowering and fruit setting.',
                'sunlight_requirements': 'Full sunlight',
                'care_instructions': 'Pruning, training, protection from mango hopper and powdery mildew.',
                'harvesting_tips': 'Harvest at mature green stage for distant markets, ripe for local consumption.',
                'is_featured': True,
            },
            {
                'name': 'Banana (అరటి)',
                'scientific_name': 'Musa spp.',
                'category': 'fruits',
                'season': 'all_season',
                'description': 'Banana is a major fruit crop providing year-round income to farmers.',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'rainfall_requirement': '1000-1500 mm',
                'soil_type': 'Deep, well-drained loamy soil',
                'ph_range': '6.0-7.5',
                'sowing_time': 'June-July, February-March',
                'harvesting_time': 'Year-round (10-12 months after planting)',
                'growth_duration': '10-12 months',
                'yield_per_acre': '25-35 tonnes',
                'watering_needs': 'Regular irrigation, maintain soil moisture throughout growth period.',
                'sunlight_requirements': 'Full sunlight',
                'care_instructions': 'Propping, desuckering, protection from sigatoka leaf spot and bunchy top virus.',
                'harvesting_tips': 'Harvest when fingers are fully developed and angular in cross-section.',
                'is_featured': False,
            },
            
            # Cash Crops
            {
                'name': 'Cotton (పత్తి)',
                'scientific_name': 'Gossypium hirsutum',
                'category': 'cash_crops',
                'season': 'kharif',
                'description': 'Cotton is a major cash crop and backbone of textile industry in Telugu states.',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'rainfall_requirement': '600-800 mm',
                'soil_type': 'Well-drained black cotton soil',
                'ph_range': '6.0-8.0',
                'sowing_time': 'June-July',
                'harvesting_time': 'October-December',
                'growth_duration': '150-180 days',
                'yield_per_acre': '8-15 quintals (seed cotton)',
                'watering_needs': 'Regular irrigation, critical at flowering and boll formation.',
                'sunlight_requirements': 'Full sunlight',
                'care_instructions': 'Thinning, weeding, protection from bollworm and sucking pests.',
                'harvesting_tips': 'Harvest when bolls are fully mature and open. Multiple pickings may be required.',
                'is_featured': True,
            },
            {
                'name': 'Sugarcane (చెరకు)',
                'scientific_name': 'Saccharum officinarum',
                'category': 'cash_crops',
                'season': 'all_season',
                'description': 'Sugarcane is a major cash crop supporting sugar industry in Telugu states.',
                'min_temperature': 20.0,
                'max_temperature': 38.0,
                'rainfall_requirement': '1500-2000 mm',
                'soil_type': 'Deep, well-drained loamy soil',
                'ph_range': '6.0-7.5',
                'sowing_time': 'February-March, June-July, October-November',
                'harvesting_time': '12-18 months after planting',
                'growth_duration': '12-18 months',
                'yield_per_acre': '80-120 tonnes',
                'watering_needs': 'Regular irrigation, maintain soil moisture throughout growth period.',
                'sunlight_requirements': 'Full sunlight',
                'care_instructions': 'Earthing up, weeding, protection from stem borer and red rot disease.',
                'harvesting_tips': 'Harvest at 12-18 months when canes are mature and sucrose content is maximum.',
                'is_featured': False,
            },
            
            # Spices
            {
                'name': 'Turmeric (పసుపు)',
                'scientific_name': 'Curcuma longa',
                'category': 'spices',
                'season': 'kharif',
                'description': 'Turmeric is an important spice crop with medicinal properties, widely grown in Telugu states.',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'rainfall_requirement': '1000-1500 mm',
                'soil_type': 'Well-drained sandy loam to clay loam',
                'ph_range': '6.0-7.5',
                'sowing_time': 'May-June',
                'harvesting_time': 'February-March',
                'growth_duration': '8-9 months',
                'yield_per_acre': '20-30 quintals (fresh rhizomes)',
                'watering_needs': 'Regular irrigation, maintain soil moisture throughout growth period.',
                'sunlight_requirements': 'Partial shade to full sunlight',
                'care_instructions': 'Weeding, earthing up, protection from rhizome rot and leaf spot.',
                'harvesting_tips': 'Harvest when leaves turn yellow and start drying. Cure rhizomes properly.',
                'is_featured': False,
            },
        ]
        
        for crop_data in crops_data:
            crop, created = Crop.objects.get_or_create(
                name=crop_data['name'],
                defaults=crop_data
            )
            if created:
                self.stdout.write(f'Created crop: {crop.name}')
            else:
                self.stdout.write(f'Crop already exists: {crop.name}')

    def create_pest_diseases(self):
        """Create sample pest and disease data"""
        
        pest_diseases_data = [
            {
                'name': 'Rice Stem Borer',
                'type': 'pest',
                'description': 'A major pest of rice causing dead hearts and white ears.',
                'symptoms': 'Dead hearts in vegetative stage, white ears in reproductive stage.',
                'severity': 'high',
                'treatment_methods': 'Use of resistant varieties, proper water management, chemical control with recommended insecticides.',
                'prevention_methods': 'Early planting, balanced fertilization, crop rotation, removal of crop residues.',
            },
            {
                'name': 'Groundnut Leaf Spot',
                'type': 'disease',
                'description': 'Fungal disease causing brown spots on leaves and defoliation.',
                'symptoms': 'Brown to black spots on leaves, premature defoliation.',
                'severity': 'medium',
                'treatment_methods': 'Fungicide application, proper spacing, balanced fertilization.',
                'prevention_methods': 'Crop rotation, seed treatment, proper field sanitation.',
            },
            {
                'name': 'Cotton Bollworm',
                'type': 'pest',
                'description': 'Major pest attacking cotton bolls and flowers.',
                'symptoms': 'Damaged flowers and bolls, entry holes in bolls.',
                'severity': 'high',
                'treatment_methods': 'Use of Bt cotton, chemical control, biological control agents.',
                'prevention_methods': 'Early planting, crop rotation, proper field sanitation.',
            },
            {
                'name': 'Tomato Early Blight',
                'type': 'disease',
                'description': 'Fungal disease causing leaf spots and defoliation.',
                'symptoms': 'Brown spots with concentric rings on leaves, defoliation.',
                'severity': 'medium',
                'treatment_methods': 'Fungicide application, proper spacing, balanced fertilization.',
                'prevention_methods': 'Crop rotation, seed treatment, proper field sanitation.',
            },
        ]
        
        for pd_data in pest_diseases_data:
            pest_disease, created = PestDisease.objects.get_or_create(
                name=pd_data['name'],
                defaults=pd_data
            )
            if created:
                self.stdout.write(f'Created pest/disease: {pest_disease.name}')
            else:
                self.stdout.write(f'Pest/disease already exists: {pest_disease.name}')

    def create_crop_advice(self):
        """Create sample crop advice"""
        
        # Get some crops to link advice to
        rice_crop = Crop.objects.filter(name__icontains='Rice').first()
        maize_crop = Crop.objects.filter(name__icontains='Maize').first()
        groundnut_crop = Crop.objects.filter(name__icontains='Groundnut').first()
        
        advice_data = [
            {
                'crop': rice_crop,
                'title': 'Rice Cultivation in Telugu States',
                'content': 'Rice is the staple food crop of Telugu states. For best results, use certified seeds, maintain proper water level, and follow recommended fertilizer schedule. Control weeds regularly and protect from stem borer.',
                'advice_type': 'cultivation_tips',
                'season': 'kharif',
                'is_featured': True,
            },
            {
                'crop': maize_crop,
                'title': 'Maize Farming Best Practices',
                'content': 'Maize responds well to balanced fertilization. Use hybrid seeds for better yield. Maintain proper spacing and control weeds. Protect from fall armyworm and other pests.',
                'advice_type': 'best_practices',
                'season': 'kharif',
                'is_featured': False,
            },
            {
                'crop': groundnut_crop,
                'title': 'Groundnut Cultivation Guide',
                'content': 'Groundnut requires well-drained soil. Use certified seeds and treat with rhizobium culture. Control weeds and protect from leaf spot diseases. Harvest at proper maturity.',
                'advice_type': 'cultivation_guide',
                'season': 'kharif',
                'is_featured': True,
            },
        ]
        
        for advice_item in advice_data:
            if advice_item['crop']:  # Only create if crop exists
                advice, created = CropAdvice.objects.get_or_create(
                    title=advice_item['title'],
                    crop=advice_item['crop'],
                    defaults=advice_item
                )
                if created:
                    self.stdout.write(f'Created advice: {advice.title}')
                else:
                    self.stdout.write(f'Advice already exists: {advice.title}')
            else:
                self.stdout.write(f'Skipping advice creation - crop not found')

    def create_crop_calendar(self):
        """Create sample crop calendar events"""
        
        # Get some crops to link calendar events to
        rice_crop = Crop.objects.filter(name__icontains='Rice').first()
        maize_crop = Crop.objects.filter(name__icontains='Maize').first()
        groundnut_crop = Crop.objects.filter(name__icontains='Groundnut').first()
        
        calendar_data = [
            {
                'crop': rice_crop,
                'title': 'Rice Sowing Season',
                'description': 'Best time to sow rice in Telugu states',
                'event_date': date(2024, 6, 15),
                'event_type': 'sowing',
                'is_recurring': True,
                'recurrence_pattern': 'Yearly in June',
            },
            {
                'crop': maize_crop,
                'title': 'Maize Harvesting',
                'description': 'Optimal time for maize harvesting',
                'event_date': date(2024, 9, 15),
                'event_type': 'harvesting',
                'is_recurring': True,
                'recurrence_pattern': 'Yearly in September',
            },
            {
                'crop': groundnut_crop,
                'title': 'Groundnut Sowing',
                'description': 'Recommended time for groundnut sowing',
                'event_date': date(2024, 6, 1),
                'event_type': 'sowing',
                'is_recurring': True,
                'recurrence_pattern': 'Yearly in June',
            },
        ]
        
        for calendar_item in calendar_data:
            if calendar_item['crop']:  # Only create if crop exists
                calendar_event, created = CropCalendar.objects.get_or_create(
                    title=calendar_item['title'],
                    crop=calendar_item['crop'],
                    event_date=calendar_item['event_date'],
                    defaults=calendar_item
                )
                if created:
                    self.stdout.write(f'Created calendar event: {calendar_event.title}')
                else:
                    self.stdout.write(f'Calendar event already exists: {calendar_event.title}')
            else:
                self.stdout.write(f'Skipping calendar event creation - crop not found')
