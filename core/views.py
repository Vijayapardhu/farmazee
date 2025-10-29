from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count
from .forms import UserProfileForm, ContactForm, CustomUserCreationForm
from .models import UserProfile, Contact, FAQ
from weather.models import WeatherData
from weather.advanced_weather_service import advanced_weather_service
from marketplace.models import Product
from schemes.models import GovernmentScheme

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
    recent_products = Product.objects.filter(is_active=True)[:5]
    
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
        'recent_products': recent_products,
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

def login_view(request):
    """Clean login supporting username or email with clear validation."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        identifier = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')

        if not identifier or not password:
            messages.error(request, 'Email/Username and password are required.')
            return render(request, 'registration/login_simple.html')

        # Try authenticate by username first, then fallback to email
        user = authenticate(request, username=identifier, password=password)
        if user is None:
            try:
                user_obj = User.objects.get(email__iexact=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is None:
            messages.error(request, 'Invalid credentials.')
            return render(request, 'registration/login_simple.html')

        if not user.is_active:
            messages.error(request, 'Your account is disabled. Please contact support.')
            return render(request, 'registration/login_simple.html')

        login(request, user)
        messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
        next_page = request.GET.get('next') or 'dashboard'
        return redirect(next_page)

    return render(request, 'registration/login_simple.html')


def register_view(request):
    """Simple registration: email unique, strong password, auto-login."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        errors = []
        if not first_name:
            errors.append('First name is required.')
        if not last_name:
            errors.append('Last name is required.')
        if not email:
            errors.append('Email is required.')
        elif '@' not in email or '.' not in email:
            errors.append('Please enter a valid email address.')
        elif User.objects.filter(email__iexact=email).exists():
            errors.append('An account with this email already exists.')

        if not password1 or not password2:
            errors.append('Both password fields are required.')
        elif password1 != password2:
            errors.append('Passwords do not match.')
        elif len(password1) < 8:
            errors.append('Password must be at least 8 characters long.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'registration/signup_new.html')

        try:
            username = email  # use email as username for simplicity
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                is_active=True,
            )

            UserProfile.objects.get_or_create(user=user)

            login(request, user)
            messages.success(request, f'Welcome to Farmazee, {user.get_full_name() or user.username}!')
            return redirect('dashboard')
        except Exception as exc:
            messages.error(request, f'Could not create account: {exc}')

    return render(request, 'registration/signup_new.html')


def logout_view(request):
    """User logout with proper cleanup"""
    from django.contrib.auth import logout
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

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


# Temporary compatibility views to satisfy legacy 'crops' namespace links
def crops_list(request):
    """Fallback view for deprecated crops list; redirect to marketplace products."""
    return redirect('marketplace:products')


def crops_detail(request, pk: int):
    """Fallback view for deprecated crops detail; redirect to marketplace products."""
    return redirect('marketplace:products')


# Temporary compatibility views to satisfy legacy 'community' namespace links
def community_home(request):
    """Fallback for community home; redirect to dashboard or home."""
    return redirect('dashboard' if request.user.is_authenticated else 'home')


def community_topic_detail(request, pk: int):
    """Fallback for community topic detail; redirect to community home fallback."""
    return redirect('dashboard' if request.user.is_authenticated else 'home')


def community_question_detail(request, pk: int):
    """Fallback for community question detail; redirect to community home fallback."""
    return redirect('dashboard' if request.user.is_authenticated else 'home')


def community_ask_question(request):
    """Fallback for community ask question; redirect to community home fallback."""
    return redirect('dashboard' if request.user.is_authenticated else 'home')


def community_events(request):
    """Fallback for community events list; redirect to community home fallback."""
    return redirect('dashboard' if request.user.is_authenticated else 'home')


def community_event_detail(request, pk: int):
    """Fallback for community event detail; redirect to community home fallback."""
    return redirect('dashboard' if request.user.is_authenticated else 'home')
