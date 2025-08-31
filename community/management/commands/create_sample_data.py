from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from community.models import ForumCategory, ForumTopic, Question, Expert, CommunityEvent
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Create sample community data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample community data...')
        
        # Get or create a test user
        user, created = User.objects.get_or_create(
            username='testfarmer',
            defaults={
                'email': 'test@farmazee.com',
                'first_name': 'Test',
                'last_name': 'Farmer',
                'is_staff': False,
                'is_superuser': False
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f'Created test user: {user.username}')
        else:
            self.stdout.write(f'Using existing test user: {user.username}')
        
        # Create forum categories
        categories_data = [
            {
                'name': 'Crop Production',
                'description': 'Discuss best practices for growing various crops',
                'icon': 'fas fa-seedling',
                'color': '#28a745'
            },
            {
                'name': 'Soil Health',
                'description': 'Share knowledge about soil management and improvement',
                'icon': 'fas fa-mountain',
                'color': '#8B4513'
            },
            {
                'name': 'Pest Management',
                'description': 'Discuss pest control methods and organic solutions',
                'icon': 'fas fa-bug',
                'color': '#dc3545'
            },
            {
                'name': 'Market & Finance',
                'description': 'Share market insights and financial advice',
                'icon': 'fas fa-chart-line',
                'color': '#17a2b8'
            }
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = ForumCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create forum topics
        topics_data = [
            {
                'title': 'Best practices for organic wheat farming',
                'content': 'I\'m planning to start organic wheat farming this season. Can anyone share their experience with organic methods? What are the key things to consider?',
                'category': categories[0]  # Crop Production
            },
            {
                'title': 'Improving soil fertility naturally',
                'content': 'My soil has become less fertile over the years. I want to improve it using natural methods. Any suggestions for organic fertilizers and soil amendments?',
                'category': categories[1]  # Soil Health
            },
            {
                'title': 'Natural pest control for vegetables',
                'content': 'I\'m growing vegetables in my backyard and facing issues with aphids and caterpillars. What are some effective natural pest control methods?',
                'category': categories[2]  # Pest Management
            },
            {
                'title': 'Crop insurance and government schemes',
                'content': 'I heard about new crop insurance schemes. Can someone explain the benefits and how to apply? Also, what other government schemes are available for farmers?',
                'category': categories[3]  # Market & Finance
            }
        ]
        
        for topic_data in topics_data:
            topic, created = ForumTopic.objects.get_or_create(
                title=topic_data['title'],
                defaults={
                    'author': user,
                    'category': topic_data['category'],
                    'content': topic_data['content']
                }
            )
            if created:
                self.stdout.write(f'Created topic: {topic.title}')
        
        # Create questions
        questions_data = [
            {
                'title': 'How to increase tomato yield?',
                'content': 'I\'m growing tomatoes but the yield is low. What can I do to increase production? I\'m using organic methods.',
                'status': 'open'
            },
            {
                'title': 'Best time to plant maize?',
                'content': 'When is the best time to plant maize in Telangana? What are the optimal weather conditions?',
                'status': 'open'
            },
            {
                'title': 'Organic pest control for rice',
                'content': 'I\'m looking for organic pest control methods for rice cultivation. Any recommendations?',
                'status': 'open'
            }
        ]
        
        for q_data in questions_data:
            question, created = Question.objects.get_or_create(
                title=q_data['title'],
                defaults={
                    'author': user,
                    'content': q_data['content'],
                    'status': q_data['status']
                }
            )
            if created:
                self.stdout.write(f'Created question: {question.title}')
        
        # Create community events
        events_data = [
            {
                'title': 'Organic Farming Workshop',
                'event_type': 'workshop',
                'description': 'Learn about organic farming methods, soil health, and natural pest control. Practical demonstrations included.',
                'location': 'Hyderabad Agricultural University',
                'event_date': timezone.now() + timedelta(days=7),
                'duration': '4 hours',
                'is_free': True
            },
            {
                'title': 'Farmer Market Day',
                'event_type': 'exhibition',
                'description': 'Direct selling opportunity for farmers. Connect with consumers and other farmers.',
                'location': 'Central Market, Hyderabad',
                'event_date': timezone.now() + timedelta(days=14),
                'duration': '8 hours',
                'is_free': True
            },
            {
                'title': 'Digital Agriculture Training',
                'event_type': 'training',
                'description': 'Learn about modern farming technologies, apps, and digital tools for agriculture.',
                'location': 'Online (Zoom)',
                'event_date': timezone.now() + timedelta(days=21),
                'duration': '2 hours',
                'is_free': True
            }
        ]
        
        for event_data in events_data:
            event, created = CommunityEvent.objects.get_or_create(
                title=event_data['title'],
                defaults={
                    'organizer': user,
                    **event_data
                }
            )
            if created:
                self.stdout.write(f'Created event: {event.title}')
        
        # Create an expert
        expert, created = Expert.objects.get_or_create(
            user=user,
            defaults={
                'specialization': 'crop_production',
                'qualifications': 'BSc Agriculture, MSc Agronomy, 15 years farming experience',
                'experience_years': 15,
                'bio': 'Experienced farmer and agricultural consultant specializing in organic farming and sustainable agriculture.',
                'is_verified': True,
                'rating': 4.8
            }
        )
        
        if created:
            self.stdout.write(f'Created expert profile for: {expert.user.username}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample community data!')
        )
        self.stdout.write('You can now test the community features with this sample data.')
