from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile, Contact, Language, Notification,
    LoanProduct, LoanApplication, InsuranceProduct, InsuranceApplication,
    StorageFacility, ProcessingService, TransportationService,
    Article, Video, FAQ, SystemSettings
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'farm_type', 'experience_years', 'land_area', 'created_at']
    list_filter = ['farm_type', 'experience_years', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone_number', 'village']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'phone_number', 'address', 'village', 'district', 'state', 'country', 'pincode')
        }),
        ('Farm Information', {
            'fields': ('land_area', 'farm_type', 'experience_years', 'primary_crop')
        }),
        ('Preferences', {
            'fields': ('preferred_language', 'sms_notifications', 'email_notifications')
        }),
        ('Profile', {
            'fields': ('profile_picture',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    list_editable = ['is_read']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'native_name', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'code', 'native_name']
    list_editable = ['is_active']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']

# Financial Services Admin
@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'loan_type', 'min_amount', 'max_amount', 'interest_rate', 'is_active']
    list_filter = ['loan_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'loan_type', 'description')
        }),
        ('Loan Details', {
            'fields': ('min_amount', 'max_amount', 'interest_rate', 'tenure_months', 'processing_fee')
        }),
        ('Requirements', {
            'fields': ('eligibility_criteria', 'required_documents')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'loan_product', 'amount_requested', 'status', 'applied_date']
    list_filter = ['status', 'applied_date', 'loan_product__loan_type']
    search_fields = ['user__username', 'loan_product__name']
    list_editable = ['status']
    readonly_fields = ['applied_date', 'approved_date', 'disbursed_date']
    
    fieldsets = (
        ('Application Details', {
            'fields': ('user', 'loan_product', 'amount_requested', 'purpose', 'status')
        }),
        ('Timestamps', {
            'fields': ('applied_date', 'approved_date', 'disbursed_date')
        }),
        ('Admin Notes', {
            'fields': ('remarks',)
        }),
    )

@admin.register(InsuranceProduct)
class InsuranceProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'insurance_type', 'coverage_amount', 'premium_amount', 'is_active']
    list_filter = ['insurance_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at']

@admin.register(InsuranceApplication)
class InsuranceApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'insurance_product', 'status', 'applied_date']
    list_filter = ['status', 'applied_date', 'insurance_product__insurance_type']
    search_fields = ['user__username', 'insurance_product__name']
    list_editable = ['status']
    readonly_fields = ['applied_date', 'approved_date']

# Post-Harvest Support Admin
@admin.register(StorageFacility)
class StorageFacilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'facility_type', 'location', 'contact_person', 'is_active']
    list_filter = ['facility_type', 'is_active', 'created_at']
    search_fields = ['name', 'location', 'contact_person']
    list_editable = ['is_active']
    readonly_fields = ['created_at']

@admin.register(ProcessingService)
class ProcessingServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'service_type', 'location', 'contact_person', 'is_active']
    list_filter = ['service_type', 'is_active', 'created_at']
    search_fields = ['name', 'location', 'contact_person']
    list_editable = ['is_active']
    readonly_fields = ['created_at']

@admin.register(TransportationService)
class TransportationServiceAdmin(admin.ModelAdmin):
    list_display = ['service_name', 'vehicle_type', 'contact_person', 'is_active']
    list_filter = ['vehicle_type', 'is_active', 'created_at']
    search_fields = ['service_name', 'contact_person']
    list_editable = ['is_active']
    readonly_fields = ['created_at']

# Knowledge & Support Admin
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'author', 'is_featured', 'is_published', 'views', 'created_at']
    list_filter = ['category', 'is_featured', 'is_published', 'created_at']
    search_fields = ['title', 'content', 'author']
    list_editable = ['is_featured', 'is_published']
    readonly_fields = ['views', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'content', 'summary', 'author')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_published')
        }),
        ('Statistics', {
            'fields': ('views',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'duration', 'is_featured', 'is_published', 'views', 'created_at']
    list_filter = ['category', 'is_featured', 'is_published', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_featured', 'is_published']
    readonly_fields = ['views', 'created_at']

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_active', 'order', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['is_active', 'order']
    readonly_fields = ['created_at']

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    """Admin interface for system settings"""
    list_display = ['site_name', 'site_description', 'maintenance_mode', 'debug_mode', 'updated_at']
    list_editable = ['maintenance_mode', 'debug_mode']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('General Settings', {
            'fields': ('site_name', 'site_description', 'site_logo', 'favicon', 'timezone', 'language', 
                      'maintenance_mode', 'maintenance_message', 'debug_mode')
        }),
        ('Security Settings', {
            'fields': ('session_timeout', 'max_login_attempts', 'password_min_length', 'require_strong_password',
                      'enable_2fa', 'enable_csrf', 'allowed_hosts')
        }),
        ('Email Configuration', {
            'fields': ('smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'from_email', 'from_name',
                      'email_use_tls', 'email_use_ssl')
        }),
        ('Notification Settings', {
            'fields': ('email_notifications', 'sms_notifications', 'push_notifications', 'admin_alerts', 'notification_email')
        }),
        ('Backup & Maintenance', {
            'fields': ('auto_backup', 'backup_frequency', 'retain_backups', 'backup_location', 'last_backup')
        }),
        ('Integrations', {
            'fields': ('openrouter_api_key', 'weather_api_key', 'google_maps_api_key', 'payment_gateway')
        }),
        ('UI/UX Customization', {
            'fields': ('primary_color', 'secondary_color', 'accent_color', 'font_family', 'enable_dark_mode', 'default_theme')
        }),
        ('Content Customization', {
            'fields': ('homepage_title', 'homepage_subtitle', 'about_page_content', 'contact_page_content', 'footer_text')
        }),
        ('Feature Toggles', {
            'fields': ('enable_marketplace', 'enable_community', 'enable_ai_chatbot', 'enable_weather',
                      'enable_soil_health', 'enable_crop_planning', 'enable_schemes')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords', 'google_analytics_id', 'facebook_pixel_id')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'youtube_url', 'linkedin_url')
        }),
        ('Legal Pages', {
            'fields': ('terms_of_service', 'privacy_policy', 'cookie_policy')
        }),
        ('Performance Settings', {
            'fields': ('enable_caching', 'cache_timeout', 'enable_compression', 'enable_minification')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Only allow one instance of system settings"""
        return not SystemSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of system settings"""
        return False

# Customize User admin
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering = ['-date_joined']

# Re-register User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Customize admin site
admin.site.site_header = "Farmazee Admin"
admin.site.site_title = "Farmazee Admin Portal"
admin.site.index_title = "Welcome to Farmazee Administration"
