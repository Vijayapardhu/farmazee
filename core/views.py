from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from .forms import UserProfileForm, ContactForm, CustomUserCreationForm
from .models import UserProfile, Contact, FAQ
from crops.models import Crop
from weather.models import WeatherData
from weather.advanced_weather_service import advanced_weather_service
from marketplace.models import Product
from schemes.models import GovernmentScheme
from community.models import ForumTopic, Question, Expert, CommunityEvent

def home(request):
    """Home page - shows landing page for non-logged in users, dashboard for logged in users"""
    if request.user.is_authenticated:
        # Show dashboard for logged in users
        return dashboard(request)
    else:
        # Show landing page for non-logged in users
        return landing_page(request)

def landing_page(request):
    """Landing page for non-logged in users"""
    # Get some sample data for the landing page
    featured_crops = Crop.objects.filter(is_featured=True)[:6]
    recent_schemes = GovernmentScheme.objects.filter(is_active=True)[:3]
    
    context = {
        'featured_crops': featured_crops,
        'recent_schemes': recent_schemes,
    }
    return render(request, 'core/simple_landing.html', context)

@login_required
def dashboard(request):
    """User dashboard"""
    # Get user's profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get recent activities and data
    recent_crops = Crop.objects.all()[:5]
    recent_topics = ForumTopic.objects.filter(is_active=True)[:3]
    recent_questions = Question.objects.filter(status='open')[:3]
    upcoming_events = CommunityEvent.objects.filter(is_active=True)[:3]
    
    # Get weather data using advanced service
    weather_data = None
    weather_recommendations = []
    try:
        weather_data = advanced_weather_service.get_current_weather("hyderabad")
        weather_recommendations = advanced_weather_service.get_farming_recommendations(weather_data)
    except Exception as e:
        print(f"Weather data error: {e}")
        weather_data = {
            'temperature': 28,
            'humidity': 65,
            'description': 'Partly Cloudy',
            'location': 'Hyderabad'
        }
    
    context = {
        'profile': profile,
        'recent_crops': recent_crops,
        'recent_topics': recent_topics,
        'recent_questions': recent_questions,
        'upcoming_events': upcoming_events,
        'weather_data': weather_data,
        'current_weather': weather_data,
        'recommendations': weather_recommendations,
        'city': 'Hyderabad'
    }
    return render(request, 'core/farmer_dashboard.html', context)

@login_required
def profile(request):
    """User profile management"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'core/profile.html', context)

def contact(request):
    """Contact page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'core/contact.html', context)

def signup(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Create user profile
                UserProfile.objects.get_or_create(user=user)
                # Log the user in directly after successful creation
                from django.contrib.auth import login
                login(request, user)
                messages.success(request, f'Welcome to Farmazee, {user.first_name}!')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
                return redirect('signup')
    else:
        form = CustomUserCreationForm()
    
    # Add Bootstrap classes to form fields
    for field_name, field in form.fields.items():
        field.widget.attrs['class'] = 'form-control'
        if field.required:
            field.widget.attrs['required'] = 'required'
    
    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)

def about(request):
    """About page"""
    return render(request, 'core/about.html')

def privacy_policy(request):
    """Privacy policy page"""
    return render(request, 'core/privacy_policy.html')

def terms_of_service(request):
    """Terms of service page"""
    return render(request, 'core/terms_of_service.html')

def faq(request):
    """FAQ page"""
    faqs = FAQ.objects.filter(is_active=True).order_by('category', 'order')
    return render(request, 'core/faq.html', {'faqs': faqs})
