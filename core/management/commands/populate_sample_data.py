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
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated sample data!')
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