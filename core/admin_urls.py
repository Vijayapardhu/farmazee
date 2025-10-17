from django.urls import path
from . import admin_views

app_name = 'admin'

urlpatterns = [
    # Main admin dashboard
    path('dashboard/', admin_views.admin_dashboard, name='dashboard'),
    
    # User management
    path('users/', admin_views.user_management, name='user_management'),
    
    # Content management
    # Crops management removed
    path('marketplace/', admin_views.marketplace_management, name='marketplace_management'),
    # Community management removed
    
    # System management
    path('settings/', admin_views.system_settings, name='system_settings'),
    path('analytics/', admin_views.analytics_dashboard, name='analytics_dashboard'),
    path('bulk-actions/', admin_views.bulk_actions, name='bulk_actions'),
    path('api/', admin_views.api_endpoints, name='api_endpoints'),
]
