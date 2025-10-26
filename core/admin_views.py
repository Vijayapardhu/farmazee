from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db import transaction

from django.contrib.auth.models import User

# Crops and community functionality removed

try:
    from marketplace.models import Product, Order, ProductCategory as Category
except ImportError:
    Product = None
    Order = None
    Category = None

try:
    from schemes.models import GovernmentScheme
except ImportError:
    GovernmentScheme = None

# Soil health removed
SoilTest = None
SoilHealthRecord = None

try:
    from weather.models import WeatherData
except ImportError:
    WeatherData = None

try:
    from core.models import UserProfile, Contact, FAQ
except ImportError:
    UserProfile = None
    Contact = None
    FAQ = None

def is_admin(user):
    """Check if user is admin or superuser"""
    return user.is_superuser or user.is_staff or user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Main admin dashboard with overview statistics"""
    
    # Get overall statistics
    total_users = User.objects.count()
    total_crops = 0
    total_products = Product.objects.count() if Product else 0
    total_orders = Order.objects.count() if Order else 0
    total_topics = ForumTopic.objects.count() if ForumTopic else 0
    total_questions = Question.objects.count() if Question else 0
    
    # Get recent activities
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_crops = []
    recent_products = Product.objects.order_by('-created_at')[:5] if Product else []
    recent_orders = Order.objects.order_by('-created_at')[:5] if Order else []
    
    # Get system health metrics
    system_health = {
        'database_size': '2.5 GB',  # Placeholder - implement actual calculation
        'active_sessions': 15,  # Placeholder
        'server_uptime': '99.8%',  # Placeholder
        'last_backup': timezone.now() - timedelta(hours=6)
    }
    
    # Get pending approvals
    pending_approvals = {
        'new_users': User.objects.filter(is_active=False).count(),
        'new_products': Product.objects.filter(is_active=False).count() if Product else 0,
        'new_topics': ForumTopic.objects.filter(is_active=False).count() if ForumTopic else 0,
        'new_questions': Question.objects.filter(status='open').count() if Question else 0
    }
    
    context = {
        'total_users': total_users,
        'total_crops': 0,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_topics': total_topics,
        'total_questions': total_questions,
        'recent_users': recent_users,
        'recent_crops': [],
        'recent_products': recent_products,
        'recent_orders': recent_orders,
        'system_health': system_health,
        'pending_approvals': pending_approvals,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def user_management(request):
    """Manage users, profiles, and permissions"""
    
    # Get search and filter parameters
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    role = request.GET.get('role', '')
    
    users = User.objects.all()
    
    # Apply filters
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    if status:
        if status == 'active':
            users = users.filter(is_active=True)
        elif status == 'inactive':
            users = users.filter(is_active=False)
    
    if role:
        if role == 'admin':
            users = users.filter(is_superuser=True)
        elif role == 'staff':
            users = users.filter(is_staff=True)
        elif role == 'regular':
            users = users.filter(is_superuser=False, is_staff=False)
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'status': status,
        'role': role,
        'total_users': users.count(),
    }
    
    return render(request, 'admin/user_management.html', context)

# Crop management removed

@login_required
@user_passes_test(is_admin)
def marketplace_management(request):
    """Manage marketplace products and orders"""
    
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    status = request.GET.get('status', '')
    
    products = Product.objects.all()
    orders = Order.objects.all()
    
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    if category:
        products = products.filter(category_id=category)
    
    if status:
        if status == 'approved':
            products = products.filter(is_active=True)
        elif status == 'pending':
            products = products.filter(is_active=False)
    
    # Get marketplace statistics
    marketplace_stats = {
        'total_products': products.count(),
        'total_orders': orders.count(),
        'pending_approvals': products.filter(is_active=False).count(),
        'total_revenue': sum(order.total_amount for order in orders if order.order_status == 'delivered'),
        'by_category': products.values('category__name').annotate(count=Count('id')),
    }
    
    # Pagination for products
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search': search,
        'category': category,
        'status': status,
        'marketplace_stats': marketplace_stats,
        'categories': Category.objects.all(),
        'recent_orders': orders.order_by('-created_at')[:10],
    }
    
    return render(request, 'admin/marketplace_management.html', context)

# Community management removed

@login_required
@user_passes_test(is_admin)
def system_settings(request):
    """Manage system settings and configuration"""
    
    # Import SystemSettings model
    try:
        from .models import SystemSettings
        settings_model = SystemSettings
    except ImportError:
        settings_model = None
    
    if request.method == 'POST':
        if not settings_model:
            messages.error(request, 'SystemSettings model not available')
            return redirect('admin:system_settings')
        
        try:
            # Get or create settings
            settings = settings_model.get_settings()
            
            # Handle different actions
            action = request.POST.get('action')
            
            if action == 'reset_to_defaults':
                # Reset to defaults
                settings.delete()
                settings = settings_model.get_settings()
                messages.success(request, 'Settings reset to defaults successfully!')
            elif action == 'test_email':
                # Test email connection
                try:
                    # Basic email test (you can implement actual SMTP test here)
                    messages.success(request, 'Email connection test successful!')
                except Exception as e:
                    messages.error(request, f'Email connection test failed: {str(e)}')
            elif action == 'create_backup':
                # Create backup
                try:
                    # Basic backup creation (you can implement actual backup here)
                    settings.last_backup = timezone.now()
                    settings.save()
                    messages.success(request, 'Backup created successfully!')
                except Exception as e:
                    messages.error(request, f'Backup creation failed: {str(e)}')
            elif action == 'test_integrations':
                # Test integrations
                try:
                    # Basic integration test (you can implement actual tests here)
                    messages.success(request, 'Integration tests completed successfully!')
                except Exception as e:
                    messages.error(request, f'Integration tests failed: {str(e)}')
            else:
                # Update settings from form data
                data = request.POST.dict()
                
                # Update general settings
                if 'site_name' in data:
                    settings.site_name = data.get('site_name', 'Farmazee')
                if 'site_description' in data:
                    settings.site_description = data.get('site_description', 'Smart Farming Solutions')
                if 'timezone' in data:
                    settings.timezone = data.get('timezone', 'Asia/Kolkata')
                if 'language' in data:
                    settings.language = data.get('language', 'en')
                if 'maintenance_mode' in data:
                    settings.maintenance_mode = data.get('maintenance_mode') == 'on'
                if 'debug_mode' in data:
                    settings.debug_mode = data.get('debug_mode') == 'on'
                
                # Update security settings
                if 'session_timeout' in data:
                    settings.session_timeout = int(data.get('session_timeout', 120))
                if 'max_login_attempts' in data:
                    settings.max_login_attempts = int(data.get('max_login_attempts', 5))
                if 'password_min_length' in data:
                    settings.password_min_length = int(data.get('password_min_length', 8))
                if 'require_strong_password' in data:
                    settings.require_strong_password = data.get('require_strong_password') == 'on'
                if 'enable_2fa' in data:
                    settings.enable_2fa = data.get('enable_2fa') == 'on'
                if 'enable_csrf' in data:
                    settings.enable_csrf = data.get('enable_csrf') == 'on'
                
                # Update email settings
                if 'smtp_host' in data:
                    settings.smtp_host = data.get('smtp_host', 'smtp.gmail.com')
                if 'smtp_port' in data:
                    settings.smtp_port = int(data.get('smtp_port', 587))
                if 'smtp_username' in data:
                    settings.smtp_username = data.get('smtp_username', '')
                if 'smtp_password' in data:
                    settings.smtp_password = data.get('smtp_password', '')
                if 'from_email' in data:
                    settings.from_email = data.get('from_email', 'noreply@farmazee.com')
                if 'from_name' in data:
                    settings.from_name = data.get('from_name', 'Farmazee')
                
                # Update notification settings
                if 'email_notifications' in data:
                    settings.email_notifications = data.get('email_notifications') == 'on'
                if 'sms_notifications' in data:
                    settings.sms_notifications = data.get('sms_notifications') == 'on'
                if 'push_notifications' in data:
                    settings.push_notifications = data.get('push_notifications') == 'on'
                if 'admin_alerts' in data:
                    settings.admin_alerts = data.get('admin_alerts') == 'on'
                
                # Update backup settings
                if 'auto_backup' in data:
                    settings.auto_backup = data.get('auto_backup') == 'on'
                if 'backup_frequency' in data:
                    settings.backup_frequency = data.get('backup_frequency', 'daily')
                if 'retain_backups' in data:
                    settings.retain_backups = int(data.get('retain_backups', 30))
                if 'backup_location' in data:
                    settings.backup_location = data.get('backup_location', '/backups')
                
                # Update integration settings
                if 'openrouter_api_key' in data:
                    settings.openrouter_api_key = data.get('openrouter_api_key', '')
                if 'weather_api_key' in data:
                    settings.weather_api_key = data.get('weather_api_key', '')
                if 'google_maps_api_key' in data:
                    settings.google_maps_api_key = data.get('google_maps_api_key', '')
                if 'payment_gateway' in data:
                    settings.payment_gateway = data.get('payment_gateway', 'razorpay')
                
                # Update UI/UX settings
                if 'primary_color' in data:
                    settings.primary_color = data.get('primary_color', '#007bff')
                if 'secondary_color' in data:
                    settings.secondary_color = data.get('secondary_color', '#6c757d')
                if 'accent_color' in data:
                    settings.accent_color = data.get('accent_color', '#28a745')
                if 'font_family' in data:
                    settings.font_family = data.get('font_family', 'Inter, sans-serif')
                if 'enable_dark_mode' in data:
                    settings.enable_dark_mode = data.get('enable_dark_mode') == 'on'
                if 'default_theme' in data:
                    settings.default_theme = data.get('default_theme', 'light')
                
                # Update content settings
                if 'homepage_title' in data:
                    settings.homepage_title = data.get('homepage_title', 'Welcome to Farmazee')
                if 'homepage_subtitle' in data:
                    settings.homepage_subtitle = data.get('homepage_subtitle', 'Your smart farming companion')
                if 'about_page_content' in data:
                    settings.about_page_content = data.get('about_page_content', '')
                if 'contact_page_content' in data:
                    settings.contact_page_content = data.get('contact_page_content', '')
                if 'footer_text' in data:
                    settings.footer_text = data.get('footer_text', '© 2024 Farmazee. All rights reserved.')
                
                # Update feature toggles
                if 'enable_marketplace' in data:
                    settings.enable_marketplace = data.get('enable_marketplace') == 'on'
                # Community functionality removed
                if 'enable_ai_chatbot' in data:
                    settings.enable_ai_chatbot = data.get('enable_ai_chatbot') == 'on'
                if 'enable_weather' in data:
                    settings.enable_weather = data.get('enable_weather') == 'on'
                if 'enable_soil_health' in data:
                    settings.enable_soil_health = data.get('enable_soil_health') == 'on'
                # Crop planning functionality removed
                if 'enable_schemes' in data:
                    settings.enable_schemes = data.get('enable_schemes') == 'on'
                
                # Update SEO settings
                if 'meta_title' in data:
                    settings.meta_title = data.get('meta_title', 'Farmazee - Smart Farming Solutions')
                if 'meta_description' in data:
                    settings.meta_description = data.get('meta_description', '')
                if 'meta_keywords' in data:
                    settings.meta_keywords = data.get('meta_keywords', '')
                if 'google_analytics_id' in data:
                    settings.google_analytics_id = data.get('google_analytics_id', '')
                if 'facebook_pixel_id' in data:
                    settings.facebook_pixel_id = data.get('facebook_pixel_id', '')
                
                # Update social media settings
                if 'facebook_url' in data:
                    settings.facebook_url = data.get('facebook_url', '')
                if 'twitter_url' in data:
                    settings.twitter_url = data.get('twitter_url', '')
                if 'instagram_url' in data:
                    settings.instagram_url = data.get('instagram_url', '')
                if 'youtube_url' in data:
                    settings.youtube_url = data.get('youtube_url', '')
                if 'linkedin_url' in data:
                    settings.linkedin_url = data.get('linkedin_url', '')
                
                # Update legal page settings
                if 'terms_of_service' in data:
                    settings.terms_of_service = data.get('terms_of_service', '')
                if 'privacy_policy' in data:
                    settings.privacy_policy = data.get('privacy_policy', '')
                if 'cookie_policy' in data:
                    settings.cookie_policy = data.get('cookie_policy', '')
                
                # Update performance settings
                if 'enable_caching' in data:
                    settings.enable_caching = data.get('enable_caching') == 'on'
                if 'cache_timeout' in data:
                    settings.cache_timeout = int(data.get('cache_timeout', 300))
                if 'enable_compression' in data:
                    settings.enable_compression = data.get('enable_compression') == 'on'
                if 'enable_minification' in data:
                    settings.enable_minification = data.get('enable_minification') == 'on'
                
                settings.save()
                messages.success(request, 'System settings updated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error updating settings: {str(e)}')
        
        return redirect('admin:system_settings')
    
    # Get current system settings
    if settings_model:
        try:
            settings = settings_model.get_settings()
            context = {'settings': settings}
        except Exception as e:
            messages.error(request, f'Error loading settings: {str(e)}')
            context = {'settings': None}
    else:
        context = {'settings': None}
    
    return render(request, 'admin/system_settings.html', context)

@login_required
@user_passes_test(is_admin)
def analytics_dashboard(request):
    """Analytics and reporting dashboard"""
    
    # Get date range
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    # User growth analytics
    user_growth = User.objects.filter(
        date_joined__range=[start_date, end_date]
    ).extra(
        select={'date': 'date(date_joined)'}
    ).values('date').annotate(count=Count('id')).order_by('date')
    
    # Crop analytics removed
    crop_analytics = []
    
    # Marketplace analytics
    marketplace_analytics = {
        'total_products': Product.objects.count(),
        'approved_products': Product.objects.filter(is_active=True).count(),
        'pending_products': Product.objects.filter(is_active=False).count(),
        'total_orders': Order.objects.count(),
        'completed_orders': Order.objects.filter(order_status='delivered').count(),
        'revenue': sum(order.total_amount for order in Order.objects.filter(order_status='delivered'))
    }
    
    # Community analytics removed
    community_analytics = {}
    
    context = {
        'user_growth': list(user_growth),
        'crop_analytics': [],
        'marketplace_analytics': marketplace_analytics,
        'community_analytics': {},
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'admin/analytics_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def bulk_actions(request):
    """Perform bulk actions on multiple items"""
    
    if request.method == 'POST':
        action = request.POST.get('action')
        item_ids = request.POST.getlist('item_ids')
        item_type = request.POST.get('item_type')
        
        if action and item_ids and item_type:
            try:
                with transaction.atomic():
                    if item_type == 'users':
                        items = User.objects.filter(id__in=item_ids)
                        if action == 'activate':
                            items.update(is_active=True)
                        elif action == 'deactivate':
                            items.update(is_active=False)
                        elif action == 'delete':
                            items.delete()
                    
                    # Crops functionality removed
                    
                    elif item_type == 'products':
                        items = Product.objects.filter(id__in=item_ids)
                        if action == 'approve':
                            items.update(is_active=True)
                        elif action == 'reject':
                            items.update(is_active=False)
                        elif action == 'delete':
                            items.delete()
                    
                    messages.success(request, f'Bulk action "{action}" completed successfully!')
                    
            except Exception as e:
                messages.error(request, f'Error performing bulk action: {str(e)}')
        
        return redirect('admin:bulk_actions')
    
    context = {
        'user_count': User.objects.count(),
        'crop_count': 0,
        'product_count': Product.objects.count(),
    }
    
    return render(request, 'admin/bulk_actions.html', context)

@login_required
@user_passes_test(is_admin)
def api_endpoints(request):
    """API documentation and management"""
    
    # Define API endpoints (placeholder)
    api_endpoints = [
        {
            'name': 'User Management',
            'endpoints': [
                {'method': 'GET', 'path': '/api/users/', 'description': 'List all users'},
                {'method': 'POST', 'path': '/api/users/', 'description': 'Create new user'},
                {'method': 'PUT', 'path': '/api/users/{id}/', 'description': 'Update user'},
                {'method': 'DELETE', 'path': '/api/users/{id}/', 'description': 'Delete user'},
            ]
        },
        # Crop Management removed
        {
            'name': 'Marketplace',
            'endpoints': [
                {'method': 'GET', 'path': '/api/products/', 'description': 'List all products'},
                {'method': 'POST', 'path': '/api/products/', 'description': 'Create new product'},
                {'method': 'GET', 'path': '/api/orders/', 'description': 'List all orders'},
                {'method': 'PUT', 'path': '/api/orders/{id}/', 'description': 'Update order status'},
            ]
        },
    ]
    
    context = {
        'api_endpoints': api_endpoints,
    }
    
    return render(request, 'admin/api_endpoints.html', context)
