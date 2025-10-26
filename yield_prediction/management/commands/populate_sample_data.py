from django.core.management.base import BaseCommand
from yield_prediction.models import CropType, SoilType, CropRecommendation

class Command(BaseCommand):
    help = 'Populate sample crop and soil data for yield prediction system'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample crop types...')
        
        # Create crop types
        crops_data = [
            {
                'name': 'Rice',
                'scientific_name': 'Oryza sativa',
                'category': 'cereal',
                'base_yield_min': 25,
                'base_yield_max': 45,
                'average_yield': 35,
                'growing_season': 'kharif',
                'maturity_days': 120,
                'water_requirement': 'high',
                'preferred_soil_types': 'Clay, Loamy',
                'ph_range_min': 5.5,
                'ph_range_max': 7.0
            },
            {
                'name': 'Wheat',
                'scientific_name': 'Triticum aestivum',
                'category': 'cereal',
                'base_yield_min': 20,
                'base_yield_max': 40,
                'average_yield': 30,
                'growing_season': 'rabi',
                'maturity_days': 150,
                'water_requirement': 'medium',
                'preferred_soil_types': 'Loamy, Sandy Loam',
                'ph_range_min': 6.0,
                'ph_range_max': 7.5
            },
            {
                'name': 'Maize',
                'scientific_name': 'Zea mays',
                'category': 'cereal',
                'base_yield_min': 30,
                'base_yield_max': 60,
                'average_yield': 45,
                'growing_season': 'kharif',
                'maturity_days': 90,
                'water_requirement': 'medium',
                'preferred_soil_types': 'Sandy Loam, Loamy',
                'ph_range_min': 5.5,
                'ph_range_max': 7.0
            },
            {
                'name': 'Tomato',
                'scientific_name': 'Solanum lycopersicum',
                'category': 'vegetable',
                'base_yield_min': 15,
                'base_yield_max': 35,
                'average_yield': 25,
                'growing_season': 'year_round',
                'maturity_days': 75,
                'water_requirement': 'medium',
                'preferred_soil_types': 'Sandy Loam, Loamy',
                'ph_range_min': 6.0,
                'ph_range_max': 7.0
            },
            {
                'name': 'Potato',
                'scientific_name': 'Solanum tuberosum',
                'category': 'vegetable',
                'base_yield_min': 20,
                'base_yield_max': 40,
                'average_yield': 30,
                'growing_season': 'rabi',
                'maturity_days': 100,
                'water_requirement': 'medium',
                'preferred_soil_types': 'Sandy Loam, Loamy',
                'ph_range_min': 5.5,
                'ph_range_max': 6.5
            }
        ]
        
        for crop_data in crops_data:
            crop, created = CropType.objects.get_or_create(
                name=crop_data['name'],
                defaults=crop_data
            )
            if created:
                self.stdout.write(f'Created crop: {crop.name}')
            else:
                self.stdout.write(f'Crop already exists: {crop.name}')
        
        self.stdout.write('Creating sample soil types...')
        
        # Create soil types
        soils_data = [
            {
                'name': 'Clay Soil',
                'description': 'Heavy soil with high water retention',
                'fertility_level': 'high',
                'water_retention': 'excellent',
                'drainage': 'poor',
                'yield_multiplier': 1.2
            },
            {
                'name': 'Loamy Soil',
                'description': 'Ideal soil with balanced properties',
                'fertility_level': 'high',
                'water_retention': 'good',
                'drainage': 'good',
                'yield_multiplier': 1.0
            },
            {
                'name': 'Sandy Soil',
                'description': 'Light soil with good drainage',
                'fertility_level': 'low',
                'water_retention': 'poor',
                'drainage': 'excellent',
                'yield_multiplier': 0.8
            },
            {
                'name': 'Sandy Loam',
                'description': 'Moderate soil with good balance',
                'fertility_level': 'medium',
                'water_retention': 'good',
                'drainage': 'good',
                'yield_multiplier': 0.9
            },
            {
                'name': 'Red Soil',
                'description': 'Common in tropical regions',
                'fertility_level': 'medium',
                'water_retention': 'good',
                'drainage': 'good',
                'yield_multiplier': 0.95
            }
        ]
        
        for soil_data in soils_data:
            soil, created = SoilType.objects.get_or_create(
                name=soil_data['name'],
                defaults=soil_data
            )
            if created:
                self.stdout.write(f'Created soil: {soil.name}')
            else:
                self.stdout.write(f'Soil already exists: {soil.name}')
        
        self.stdout.write('Creating crop recommendations...')
        
        # Create crop recommendations
        clay_soil = SoilType.objects.get(name='Clay Soil')
        loamy_soil = SoilType.objects.get(name='Loamy Soil')
        sandy_soil = SoilType.objects.get(name='Sandy Soil')
        
        rice = CropType.objects.get(name='Rice')
        wheat = CropType.objects.get(name='Wheat')
        maize = CropType.objects.get(name='Maize')
        tomato = CropType.objects.get(name='Tomato')
        potato = CropType.objects.get(name='Potato')
        
        # Kharif season recommendations
        kharif_recommendations = [
            {
                'soil_type': clay_soil,
                'season': 'kharif',
                'recommended_crops': [rice, maize],
                'description': 'Clay soil is excellent for rice and maize during monsoon season'
            },
            {
                'soil_type': loamy_soil,
                'season': 'kharif',
                'recommended_crops': [rice, maize, tomato],
                'description': 'Loamy soil supports all major kharif crops'
            },
            {
                'soil_type': sandy_soil,
                'season': 'kharif',
                'recommended_crops': [maize, tomato],
                'description': 'Sandy soil is suitable for maize and vegetables'
            }
        ]
        
        # Rabi season recommendations
        rabi_recommendations = [
            {
                'soil_type': clay_soil,
                'season': 'rabi',
                'recommended_crops': [wheat, potato],
                'description': 'Clay soil retains moisture well for winter crops'
            },
            {
                'soil_type': loamy_soil,
                'season': 'rabi',
                'recommended_crops': [wheat, potato, tomato],
                'description': 'Loamy soil is ideal for all rabi crops'
            },
            {
                'soil_type': sandy_soil,
                'season': 'rabi',
                'recommended_crops': [wheat, tomato],
                'description': 'Sandy soil works well for wheat and vegetables'
            }
        ]
        
        all_recommendations = kharif_recommendations + rabi_recommendations
        
        for rec_data in all_recommendations:
            rec, created = CropRecommendation.objects.get_or_create(
                soil_type=rec_data['soil_type'],
                season=rec_data['season'],
                defaults={
                    'description': rec_data['description']
                }
            )
            if created:
                rec.recommended_crops.set(rec_data['recommended_crops'])
                self.stdout.write(f'Created recommendation: {rec.soil_type.name} - {rec.get_season_display()}')
            else:
                self.stdout.write(f'Recommendation already exists: {rec.soil_type.name} - {rec.get_season_display()}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample data for yield prediction system!')
        )


