from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Count
from .forms import UserProfileForm, ContactForm, CustomUserCreationForm
from .models import UserProfile, Contact, FAQ
from weather.models import WeatherData
from weather.advanced_weather_service import advanced_weather_service
# from marketplace.models import Product  # Removed - marketplace now uses irrigation reminders
from schemes.models import GovernmentScheme
from django.conf import settings
import json
from pathlib import Path

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
    recent_schemes = GovernmentScheme.objects.filter(is_active=True)[:3]
    
    context = {
        'recent_schemes': recent_schemes,
    }
    return render(request, 'core/simple_landing.html', context)

@login_required
def dashboard(request):
    """User dashboard"""
    # Get user's profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get recent activities and data
    try:
        from marketplace.models import IrrigationReminder  # marketplace may be removed
        recent_reminders = IrrigationReminder.objects.filter(user=request.user, status='active')[:5]
    except Exception:
        recent_reminders = []
    
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
        'recent_reminders': recent_reminders,
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
            return redirect('core:profile')
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
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'core/contact.html', context)

def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    form = AuthenticationForm(request=request, data=request.POST or None)
    # Add Bootstrap classes to form fields for better UX
    for field_name, field in form.fields.items():
        existing_classes = field.widget.attrs.get('class', '')
        field.widget.attrs['class'] = (existing_classes + ' form-control').strip()
        if field.required:
            field.widget.attrs['required'] = 'required'
        # Helpful placeholders
        if field_name == 'username' and 'placeholder' not in field.widget.attrs:
            field.widget.attrs['placeholder'] = 'Username or Email'
        if field_name == 'password' and 'placeholder' not in field.widget.attrs:
            field.widget.attrs['placeholder'] = 'Password'
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.get_short_name() or user.username}!')
        next_url = request.POST.get('next') or request.GET.get('next')
        return redirect(next_url or 'core:dashboard')

    context = {
        'form': form,
    }
    return render(request, 'core/login.html', context)

def logout_view(request):
    """User logout"""
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('core:home')

def signup(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)

            # Auto-login and redirect
            raw_password = form.cleaned_data.get('password1')
            auth_user = authenticate(request, username=user.username, password=raw_password)
            if auth_user is not None:
                login(request, auth_user)
            else:
                # Fallback if multiple auth backends
                login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])

            messages.success(request, f'Welcome to Farmazee, {user.first_name or user.username}!')
            next_param = request.POST.get('next') or request.GET.get('next')
            return redirect(next_param or 'core:dashboard')
        # If invalid, fall through to render form with errors
    else:
        form = CustomUserCreationForm()

    # Add Bootstrap classes to form fields
    for field_name, field in form.fields.items():
        field.widget.attrs['class'] = 'form-control'
        if field.required:
            field.widget.attrs['required'] = 'required'

    context = {
        'form': form,
        'debug': settings.DEBUG,
    }
    return render(request, 'core/signup_simple.html', context)

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
def crop_planner(request):
    """Smart Crop Planner: suggests suitable crops based on land, soil, season."""
    data_path = Path(settings.BASE_DIR) / 'static' / 'data' / 'crops.json'
    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            crops = json.load(f)
    except Exception:
        crops = []

    results = []
    input_land = 0.0
    soil = ''
    season = ''

    # Accept both POST (form submit) and GET (after choosing a crop) flows
    params = request.POST if request.method == 'POST' else request.GET
    if params.get('land_size') and params.get('soil_type') and params.get('season'):
        try:
            input_land = float(params.get('land_size', '0') or 0)
        except ValueError:
            input_land = 0.0
        soil = (params.get('soil_type', '') or '').strip().lower()
        season = (params.get('season', '') or '').strip().lower()

        for c in crops:
            if (soil in [s.lower() for s in c.get('soil_types', [])]) and (season in [s.lower() for s in c.get('seasons', [])]):
                yield_per_acre = c.get('expected_yield_quintal_per_acre', 0)
                price_per_quintal = c.get('expected_market_price_per_quintal', 0)
                total_yield = yield_per_acre * input_land
                gross_revenue = total_yield * price_per_quintal
                results.append({
                    'name': c.get('name'),
                    'expected_yield_quintal_per_acre': yield_per_acre,
                    'expected_market_price_per_quintal': price_per_quintal,
                    'total_expected_yield_quintal': total_yield,
                    'gross_revenue_inr': gross_revenue,
                    'tips': c.get('tips', '')
                })

        # Sort by gross revenue desc
        results.sort(key=lambda x: x['gross_revenue_inr'], reverse=True)

    context = {
        'results': results,
        'land_size': input_land,
        'soil_type': soil,
        'season': season,
        'crops': crops,
        'selected_crop': request.GET.get('crop') or request.POST.get('crop') or '',
    }
    return render(request, 'core/crop_planner.html', context)

