from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from crops.models import Crop
from django.utils import timezone


class Command(BaseCommand):
    help = 'Create sample crop data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample crop data...')
        
        # Sample crops data
        crops_data = [
            {
                'name': 'Wheat',
                'scientific_name': 'Triticum aestivum',
                'category': 'cereals',
                'season': 'rabi',
                'description': 'Wheat is a cereal grain that is a worldwide staple food. It is the most widely grown crop in the world.',
                'min_temperature': 15.0,
                'max_temperature': 25.0,
                'rainfall_requirement': '400-600 mm',
                'soil_type': 'Well-drained loamy soil',
                'ph_range': '6.0-7.5',
                'sowing_time': 'November to December',
                'harvesting_time': 'March to April',
                'growth_duration': '120-150 days',
                'yield_per_acre': '15-20 quintals',
                'watering_needs': 'Regular irrigation needed, especially during flowering and grain filling stages',
                'sunlight_requirements': 'Full sun (6-8 hours daily)',
                'care_instructions': 'Regular weeding, pest control, and balanced fertilization required',
                'harvesting_tips': 'Harvest when grains are hard and moisture content is around 14%',
                'is_featured': True
            },
            {
                'name': 'Rice',
                'scientific_name': 'Oryza sativa',
                'category': 'cereals',
                'season': 'kharif',
                'description': 'Rice is the seed of the grass species Oryza sativa. It is the most important grain with regard to human nutrition.',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'rainfall_requirement': '1000-1500 mm',
                'soil_type': 'Clay loam soil with good water retention',
                'ph_range': '5.5-6.5',
                'sowing_time': 'June to July',
                'harvesting_time': 'October to November',
                'growth_duration': '120-150 days',
                'yield_per_acre': '25-30 quintals',
                'watering_needs': 'Continuous flooding or alternate wetting and drying',
                'sunlight_requirements': 'Full sun (8-10 hours daily)',
                'care_instructions': 'Proper water management, weed control, and balanced fertilization',
                'harvesting_tips': 'Harvest when 80-85% of grains are mature',
                'is_featured': True
            },
            {
                'name': 'Tomato',
                'scientific_name': 'Solanum lycopersicum',
                'category': 'vegetables',
                'season': 'all_season',
                'description': 'Tomato is a red, edible berry of the plant Solanum lycopersicum. It is rich in lycopene and vitamin C.',
                'min_temperature': 18.0,
                'max_temperature': 30.0,
                'rainfall_requirement': '600-800 mm',
                'soil_type': 'Well-drained sandy loam soil',
                'ph_range': '6.0-7.0',
                'sowing_time': 'Year-round (avoid extreme weather)',
                'harvesting_time': '70-90 days after transplanting',
                'growth_duration': '70-90 days',
                'yield_per_acre': '15-20 tons',
                'watering_needs': 'Regular watering, avoid waterlogging',
                'sunlight_requirements': 'Full sun (6-8 hours daily)',
                'care_instructions': 'Staking, pruning, pest control, and balanced fertilization',
                'harvesting_tips': 'Harvest when fruits are firm and fully colored',
                'is_featured': True
            },
            {
                'name': 'Cotton',
                'scientific_name': 'Gossypium hirsutum',
                'category': 'cash_crops',
                'season': 'kharif',
                'description': 'Cotton is a soft, fluffy staple fiber that grows in a boll around the seeds of cotton plants.',
                'min_temperature': 20.0,
                'max_temperature': 35.0,
                'rainfall_requirement': '800-1200 mm',
                'soil_type': 'Deep, well-drained black soil',
                'ph_range': '6.0-8.0',
                'sowing_time': 'May to June',
                'harvesting_time': 'October to December',
                'growth_duration': '150-180 days',
                'yield_per_acre': '8-12 quintals',
                'watering_needs': 'Critical stages: flowering and boll development',
                'sunlight_requirements': 'Full sun (8-10 hours daily)',
                'care_instructions': 'Pest control, weed management, and balanced fertilization',
                'harvesting_tips': 'Harvest when bolls are fully open and fibers are mature',
                'is_featured': False
            },
            {
                'name': 'Sugarcane',
                'scientific_name': 'Saccharum officinarum',
                'category': 'cash_crops',
                'season': 'all_season',
                'description': 'Sugarcane is a tall perennial grass that is cultivated for its juice, from which sugar is processed.',
                'min_temperature': 20.0,
                'max_temperature': 38.0,
                'rainfall_requirement': '1500-2000 mm',
                'soil_type': 'Deep, well-drained loamy soil',
                'ph_range': '6.0-7.5',
                'sowing_time': 'February to March (Spring) or September to October (Autumn)',
                'harvesting_time': '12-18 months after planting',
                'growth_duration': '12-18 months',
                'yield_per_acre': '60-80 tons',
                'watering_needs': 'Regular irrigation, especially during growth phase',
                'sunlight_requirements': 'Full sun (8-10 hours daily)',
                'care_instructions': 'Weed control, pest management, and balanced fertilization',
                'harvesting_tips': 'Harvest when canes are mature and sugar content is optimal',
                'is_featured': False
            }
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
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample crop data!')
        )
        self.stdout.write('You can now test the crop features with this sample data.')
