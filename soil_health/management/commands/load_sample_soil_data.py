from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from soil_health.models import (
    SoilType, SoilTip, SoilTest, SoilTestResult, 
    SoilHealthRecord, FertilizerRecommendation
)
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Load sample soil health data for demonstration'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample soil health data...')
        
        # Create soil types if they don't exist
        soil_types = self.create_soil_types()
        
        # Create soil tips
        self.create_soil_tips()
        
        # Create sample soil tests and results
        self.create_sample_soil_tests(soil_types)
        
        # Create soil health records
        self.create_soil_health_records(soil_types)
        
        # Create fertilizer recommendations
        self.create_fertilizer_recommendations()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample soil health data!')
        )

    def create_soil_types(self):
        """Create different soil types"""
        soil_types_data = [
            {
                'name': 'Clay Loam',
                'description': 'Rich in nutrients, good water retention, suitable for rice and vegetables'
            },
            {
                'name': 'Sandy Loam',
                'description': 'Well-draining, good for root crops and vegetables, requires more irrigation'
            },
            {
                'name': 'Red Soil',
                'description': 'Common in Telugu states, good for cotton, groundnut, and pulses'
            },
            {
                'name': 'Black Soil',
                'description': 'Rich in minerals, excellent for cotton, sugarcane, and oilseeds'
            },
            {
                'name': 'Alluvial Soil',
                'description': 'Fertile soil found near rivers, suitable for all types of crops'
            }
        ]
        
        soil_types = []
        for data in soil_types_data:
            soil_type, created = SoilType.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created soil type: {soil_type.name}')
            soil_types.append(soil_type)
        
        return soil_types

    def create_soil_tips(self):
        """Create soil health tips"""
        tips_data = [
            {
                'title': 'Optimal pH for Different Crops',
                'category': 'testing',
                'content': 'Most crops prefer pH 6.0-7.5. Rice grows well in slightly acidic soil (5.5-6.5), while cotton prefers neutral to slightly alkaline soil (6.5-7.5).',
                'is_featured': True
            },
            {
                'title': 'Organic Matter Improvement',
                'category': 'improvement',
                'content': 'Add farmyard manure, compost, or green manure crops to increase organic matter content. Aim for 2-3% organic matter for optimal soil health.',
                'is_featured': True
            },
            {
                'title': 'Nutrient Deficiency Symptoms',
                'category': 'nutrients',
                'content': 'Yellow leaves often indicate nitrogen deficiency. Purple leaves suggest phosphorus deficiency. Brown leaf edges may indicate potassium deficiency.',
                'is_featured': False
            },
            {
                'title': 'Soil Testing Frequency',
                'category': 'testing',
                'content': 'Test your soil every 2-3 years for major nutrients (NPK) and pH. Test annually if you notice crop problems or after major soil amendments.',
                'is_featured': False
            },
            {
                'title': 'Water Conservation in Soil',
                'category': 'conservation',
                'content': 'Use mulching to reduce water evaporation. Practice contour farming on slopes. Implement drip irrigation for water efficiency.',
                'is_featured': False
            }
        ]
        
        for data in tips_data:
            tip, created = SoilTip.objects.get_or_create(
                title=data['title'],
                defaults=data
            )
            if created:
                self.stdout.write(f'Created soil tip: {tip.title}')

    def create_sample_soil_tests(self, soil_types):
        """Create sample soil tests with results"""
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='demo_farmer',
            defaults={
                'email': 'demo@farmazee.com',
                'first_name': 'Demo',
                'last_name': 'Farmer'
            }
        )
        
        if created:
            user.set_password('demo123')
            user.save()
            self.stdout.write('Created demo user: demo_farmer')
        
        # Create sample soil tests
        test_locations = ['North Field', 'South Field', 'East Plot', 'West Garden', 'Central Farm']
        test_types = ['ph', 'npk', 'organic_matter', 'comprehensive']
        
        for i in range(5):
            test_date = date.today() - timedelta(days=random.randint(30, 365))
            test_type = random.choice(test_types)
            location = random.choice(test_locations)
            soil_type = random.choice(soil_types)
            
            test = SoilTest.objects.create(
                user=user,
                test_type=test_type,
                test_date=test_date,
                location=location,
                soil_depth=random.choice(['0-15 cm', '15-30 cm', '30-60 cm']),
                sample_weight=f"{random.randint(500, 1000)}g",
                notes=f"Sample collected from {location} for {test_type} analysis",
                is_completed=True
            )
            
            # Create test results based on test type
            if test_type == 'ph':
                self.create_ph_test_results(test)
            elif test_type == 'npk':
                self.create_npk_test_results(test)
            elif test_type == 'organic_matter':
                self.create_organic_matter_test_results(test)
            else:  # comprehensive
                self.create_comprehensive_test_results(test)
            
            self.stdout.write(f'Created soil test: {test.get_test_type_display()} at {location}')

    def create_ph_test_results(self, test):
        """Create pH test results"""
        ph_value = round(random.uniform(5.5, 8.0), 1)
        status = 'optimal' if 6.0 <= ph_value <= 7.5 else 'low' if ph_value < 6.0 else 'high'
        
        SoilTestResult.objects.create(
            soil_test=test,
            parameter='ph',
            value=ph_value,
            unit='-',
            status=status,
            recommendation=self.get_ph_recommendation(ph_value)
        )

    def create_npk_test_results(self, test):
        """Create NPK test results"""
        # Nitrogen
        n_value = round(random.uniform(20, 80), 1)
        n_status = 'low' if n_value < 40 else 'medium' if n_value < 60 else 'high'
        SoilTestResult.objects.create(
            soil_test=test,
            parameter='nitrogen',
            value=n_value,
            unit='kg/ha',
            status=n_status,
            recommendation=self.get_npk_recommendation('nitrogen', n_value)
        )
        
        # Phosphorus
        p_value = round(random.uniform(15, 60), 1)
        p_status = 'low' if p_value < 25 else 'medium' if p_value < 40 else 'high'
        SoilTestResult.objects.create(
            soil_test=test,
            parameter='phosphorus',
            value=p_value,
            unit='kg/ha',
            status=p_status,
            recommendation=self.get_npk_recommendation('phosphorus', p_value)
        )
        
        # Potassium
        k_value = round(random.uniform(25, 100), 1)
        k_status = 'low' if k_value < 40 else 'medium' if k_value < 70 else 'high'
        SoilTestResult.objects.create(
            soil_test=test,
            parameter='potassium',
            value=k_value,
            unit='kg/ha',
            status=k_status,
            recommendation=self.get_npk_recommendation('potassium', k_value)
        )

    def create_organic_matter_test_results(self, test):
        """Create organic matter test results"""
        om_value = round(random.uniform(1.0, 4.0), 2)
        status = 'low' if om_value < 1.5 else 'medium' if om_value < 2.5 else 'high'
        
        SoilTestResult.objects.create(
            soil_test=test,
            parameter='organic_matter',
            value=om_value,
            unit='%',
            status=status,
            recommendation=self.get_organic_matter_recommendation(om_value)
        )

    def create_comprehensive_test_results(self, test):
        """Create comprehensive test results"""
        # Create all major parameters
        self.create_ph_test_results(test)
        self.create_npk_test_results(test)
        self.create_organic_matter_test_results(test)
        
        # Add micronutrients
        micronutrients = ['calcium', 'magnesium', 'sulfur', 'zinc', 'iron']
        for nutrient in micronutrients:
            value = round(random.uniform(10, 100), 1)
            status = 'low' if value < 30 else 'medium' if value < 70 else 'high'
            
            SoilTestResult.objects.create(
                soil_test=test,
                parameter=nutrient,
                value=value,
                unit='ppm' if nutrient in ['zinc', 'iron'] else 'meq/100g',
                status=status,
                recommendation=f"Maintain current {nutrient} levels for optimal crop growth."
            )

    def create_soil_health_records(self, soil_types):
        """Create soil health monitoring records"""
        user = User.objects.get(username='demo_farmer')
        
        for i in range(3):
            record_date = date.today() - timedelta(days=random.randint(30, 180))
            location = random.choice(['North Field', 'South Field', 'East Plot'])
            soil_type = random.choice(soil_types)
            
            # Generate realistic soil health data
            ph_level = round(random.uniform(6.0, 7.5), 1)
            organic_matter = round(random.uniform(1.5, 3.0), 2)
            nitrogen = round(random.uniform(30, 70), 1)
            phosphorus = round(random.uniform(20, 50), 1)
            potassium = round(random.uniform(40, 80), 1)
            
            # Calculate health score based on parameters
            health_score = self.calculate_health_score(ph_level, organic_matter, nitrogen, phosphorus, potassium)
            is_healthy = health_score >= 7
            
            SoilHealthRecord.objects.create(
                user=user,
                record_date=record_date,
                location=location,
                soil_type=soil_type,
                ph_level=ph_level,
                organic_matter=organic_matter,
                nitrogen=nitrogen,
                phosphorus=phosphorus,
                potassium=potassium,
                is_healthy=is_healthy,
                health_score=health_score,
                notes=f"Regular soil health monitoring at {location}. Overall soil condition is {'good' if is_healthy else 'needs improvement'}."
            )
            
            self.stdout.write(f'Created soil health record for {location}')

    def create_fertilizer_recommendations(self):
        """Create sample fertilizer recommendations"""
        recommendations_data = [
            {
                'fertilizer_name': 'Urea (46-0-0)',
                'application_rate': '100-150 kg/ha',
                'application_method': 'Broadcast before sowing',
                'recommendation': 'Apply urea for nitrogen-deficient soils. Split application recommended for better efficiency.',
                'precautions': 'Avoid application during heavy rains. Keep away from direct contact with seeds.'
            },
            {
                'fertilizer_name': 'DAP (18-46-0)',
                'application_rate': '120-180 kg/ha',
                'application_method': 'Band placement at sowing',
                'recommendation': 'Excellent source of phosphorus. Apply at sowing for better root development.',
                'precautions': 'Store in dry place. Avoid mixing with seeds.'
            },
            {
                'fertilizer_name': 'MOP (0-0-60)',
                'application_rate': '80-120 kg/ha',
                'application_method': 'Broadcast or band placement',
                'recommendation': 'Essential for potassium supply. Apply before sowing or as top dressing.',
                'precautions': 'Apply in split doses for better efficiency.'
            },
            {
                'fertilizer_name': 'Farmyard Manure',
                'application_rate': '5-10 tonnes/ha',
                'application_method': 'Broadcast and incorporate',
                'recommendation': 'Excellent for improving soil structure and organic matter content.',
                'precautions': 'Ensure proper decomposition before application.'
            }
        ]
        
        # Get a sample test result to link recommendations
        test_results = SoilTestResult.objects.filter(parameter='nitrogen')[:1]
        if test_results.exists():
            for data in recommendations_data:
                recommendation = FertilizerRecommendation.objects.create(
                    soil_test_result=test_results[0],
                    **data
                )
                self.stdout.write(f'Created fertilizer recommendation: {recommendation.fertilizer_name}')

    def get_ph_recommendation(self, ph_value):
        """Get pH-specific recommendations"""
        if ph_value < 6.0:
            return "Soil is acidic. Apply agricultural lime (CaCO3) at 2-4 tonnes/ha to raise pH. Retest after 3-6 months."
        elif ph_value > 7.5:
            return "Soil is alkaline. Apply elemental sulfur or organic matter to lower pH. Consider acid-loving crops."
        else:
            return "pH is optimal for most crops. Maintain current levels with regular monitoring."

    def get_npk_recommendation(self, nutrient, value):
        """Get NPK-specific recommendations"""
        if nutrient == 'nitrogen':
            if value < 40:
                return "Apply nitrogen fertilizers like urea (100-150 kg/ha) or organic sources like farmyard manure."
            elif value < 60:
                return "Moderate nitrogen levels. Apply 50-75 kg/ha urea for heavy feeders like rice and maize."
            else:
                return "Adequate nitrogen levels. Maintain with organic sources and crop rotation."
        
        elif nutrient == 'phosphorus':
            if value < 25:
                return "Apply phosphorus fertilizers like DAP (120-180 kg/ha) or rock phosphate for organic farming."
            elif value < 40:
                return "Moderate phosphorus levels. Apply 60-90 kg/ha DAP for better root development."
            else:
                return "Sufficient phosphorus levels. Focus on maintaining organic matter content."
        
        elif nutrient == 'potassium':
            if value < 40:
                return "Apply potassium fertilizers like MOP (80-120 kg/ha) for better crop quality and disease resistance."
            elif value < 70:
                return "Moderate potassium levels. Apply 40-60 kg/ha MOP for heavy feeders."
            else:
                return "Adequate potassium levels. Maintain with regular soil testing."

    def get_organic_matter_recommendation(self, om_value):
        """Get organic matter recommendations"""
        if om_value < 1.5:
            return "Low organic matter. Apply farmyard manure (5-10 tonnes/ha), compost, or grow green manure crops."
        elif om_value < 2.5:
            return "Moderate organic matter. Maintain with regular addition of organic materials and crop residues."
        else:
            return "Good organic matter content. Continue with sustainable practices and regular monitoring."

    def calculate_health_score(self, ph, om, n, p, k):
        """Calculate soil health score based on parameters"""
        score = 0
        
        # pH score (0-2 points)
        if 6.0 <= ph <= 7.5:
            score += 2
        elif 5.5 <= ph <= 8.0:
            score += 1
        
        # Organic matter score (0-2 points)
        if om >= 2.5:
            score += 2
        elif om >= 1.5:
            score += 1
        
        # NPK score (0-6 points)
        if 40 <= n <= 70:
            score += 2
        elif 30 <= n <= 80:
            score += 1
        
        if 25 <= p <= 50:
            score += 2
        elif 20 <= p <= 60:
            score += 1
        
        if 40 <= k <= 80:
            score += 2
        elif 30 <= k <= 90:
            score += 1
        
        return min(score, 10)  # Cap at 10
