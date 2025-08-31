from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
from django_countries.fields import CountryField


class Language(models.Model):
    """Language model for multilingual support"""
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=50)
    native_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')
    
    def __str__(self):
        return f"{self.name} ({self.code})"


class UserProfile(models.Model):
    """Extended user profile for farmers"""
    FARM_TYPES = [
        ('small', 'Small Scale (< 2 acres)'),
        ('medium', 'Medium Scale (2-10 acres)'),
        ('large', 'Large Scale (> 10 acres)'),
        ('organic', 'Organic Farming'),
        ('commercial', 'Commercial Farming'),
        ('subsistence', 'Subsistence Farming'),
    ]
    
    EXPERIENCE_LEVELS = [
        ('beginner', 'Beginner (0-2 years)'),
        ('intermediate', 'Intermediate (3-5 years)'),
        ('experienced', 'Experienced (6-10 years)'),
        ('expert', 'Expert (10+ years)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    village = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = CountryField(default='IN')
    pincode = models.CharField(max_length=10, blank=True, null=True)
    land_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Land area in acres')
    primary_crop = models.CharField(max_length=100, blank=True, null=True)
    farm_type = models.CharField(max_length=20, choices=FARM_TYPES, blank=True, null=True)
    experience_years = models.CharField(max_length=20, choices=EXPERIENCE_LEVELS, blank=True, null=True)
    preferred_language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, blank=True)
    sms_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.village}"


class Notification(models.Model):
    """Notification system for users"""
    NOTIFICATION_TYPES = [
        ('weather', 'Weather Alert'),
        ('market', 'Market Update'),
        ('scheme', 'Government Scheme'),
        ('crop', 'Crop Advisory'),
        ('community', 'Community Update'),
        ('financial', 'Financial Update'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class Contact(models.Model):
    """Contact form submissions"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"


# Financial Services Models
class LoanProduct(models.Model):
    """Loan products for farmers"""
    LOAN_TYPES = [
        ('crop', 'Crop Loan'),
        ('equipment', 'Equipment Loan'),
        ('infrastructure', 'Infrastructure Loan'),
        ('emergency', 'Emergency Loan'),
        ('organic', 'Organic Farming Loan'),
    ]
    
    name = models.CharField(max_length=200)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    description = models.TextField()
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text='Annual interest rate in percentage')
    tenure_months = models.IntegerField(help_text='Loan tenure in months')
    processing_fee = models.DecimalField(max_digits=5, decimal_places=2, help_text='Processing fee in percentage')
    eligibility_criteria = models.TextField()
    required_documents = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.get_loan_type_display()}"


class LoanApplication(models.Model):
    """Loan applications by farmers"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('closed', 'Closed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_applications')
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE)
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    purpose = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    disbursed_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-applied_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.loan_product.name} - {self.status}"


class InsuranceProduct(models.Model):
    """Insurance products for farmers"""
    INSURANCE_TYPES = [
        ('crop', 'Crop Insurance'),
        ('livestock', 'Livestock Insurance'),
        ('equipment', 'Equipment Insurance'),
        ('health', 'Health Insurance'),
        ('life', 'Life Insurance'),
    ]
    
    name = models.CharField(max_length=200)
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPES)
    description = models.TextField()
    coverage_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium_amount = models.DecimalField(max_digits=8, decimal_places=2)
    coverage_period = models.CharField(max_length=100)
    terms_conditions = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.get_insurance_type_display()}"


class InsuranceApplication(models.Model):
    """Insurance applications by farmers"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insurance_applications')
    insurance_product = models.ForeignKey(InsuranceProduct, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-applied_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.insurance_product.name} - {self.status}"


# Post-Harvest Support Models
class StorageFacility(models.Model):
    """Storage facilities for post-harvest management"""
    FACILITY_TYPES = [
        ('warehouse', 'Warehouse'),
        ('cold_storage', 'Cold Storage'),
        ('silo', 'Silo'),
        ('godown', 'Godown'),
        ('processing_unit', 'Processing Unit'),
    ]
    
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=20, choices=FACILITY_TYPES)
    location = models.CharField(max_length=200)
    capacity = models.CharField(max_length=100, help_text='Storage capacity')
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    description = models.TextField()
    services_offered = models.TextField()
    pricing = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Storage Facilities'
    
    def __str__(self):
        return f"{self.name} - {self.get_facility_type_display()}"


class ProcessingService(models.Model):
    """Processing services for agricultural products"""
    SERVICE_TYPES = [
        ('cleaning', 'Cleaning & Grading'),
        ('packaging', 'Packaging'),
        ('drying', 'Drying'),
        ('milling', 'Milling'),
        ('oil_extraction', 'Oil Extraction'),
        ('preservation', 'Preservation'),
    ]
    
    name = models.CharField(max_length=200)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()
    suitable_crops = models.TextField()
    processing_capacity = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    location = models.CharField(max_length=200)
    pricing = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.get_service_type_display()}"


class TransportationService(models.Model):
    """Transportation services for agricultural products"""
    VEHICLE_TYPES = [
        ('truck', 'Truck'),
        ('tractor_trailer', 'Tractor Trailer'),
        ('mini_truck', 'Mini Truck'),
        ('refrigerated', 'Refrigerated Vehicle'),
        ('bulk_carrier', 'Bulk Carrier'),
    ]
    
    service_name = models.CharField(max_length=200)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    capacity = models.CharField(max_length=100)
    service_areas = models.TextField()
    contact_person = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    pricing = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['service_name']
    
    def __str__(self):
        return f"{self.service_name} - {self.get_vehicle_type_display()}"


# Knowledge & Support Models
class Article(models.Model):
    """Educational articles and guides"""
    CATEGORIES = [
        ('farming_techniques', 'Farming Techniques'),
        ('crop_management', 'Crop Management'),
        ('soil_health', 'Soil Health'),
        ('pest_management', 'Pest Management'),
        ('technology', 'Technology'),
        ('sustainability', 'Sustainability'),
        ('market_trends', 'Market Trends'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Video(models.Model):
    """Educational videos"""
    CATEGORIES = [
        ('tutorial', 'Tutorial'),
        ('demonstration', 'Demonstration'),
        ('expert_talk', 'Expert Talk'),
        ('success_story', 'Success Story'),
        ('technology', 'Technology'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    description = models.TextField()
    video_url = models.URLField()
    thumbnail = models.ImageField(upload_to='videos/', blank=True, null=True)
    duration = models.CharField(max_length=20, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class FAQ(models.Model):
    """Frequently Asked Questions"""
    CATEGORIES = [
        ('general', 'General'),
        ('crops', 'Crops'),
        ('weather', 'Weather'),
        ('market', 'Market'),
        ('financial', 'Financial'),
        ('technical', 'Technical'),
    ]
    
    question = models.TextField()
    answer = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'question']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
    
    def __str__(self):
        return self.question[:100] + "..." if len(self.question) > 100 else self.question


class SystemSettings(models.Model):
    """System-wide settings and configuration"""
    
    # General Settings
    site_name = models.CharField(max_length=100, default='Farmazee')
    site_description = models.TextField(default='Smart Farming Solutions')
    site_logo = models.ImageField(upload_to='site/', null=True, blank=True)
    favicon = models.ImageField(upload_to='site/', null=True, blank=True)
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    language = models.CharField(max_length=10, default='en')
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(default='Site is under maintenance. Please check back later.')
    debug_mode = models.BooleanField(default=False)
    
    # Security Settings
    session_timeout = models.IntegerField(default=120)  # minutes
    max_login_attempts = models.IntegerField(default=5)
    password_min_length = models.IntegerField(default=8)
    require_strong_password = models.BooleanField(default=True)
    enable_2fa = models.BooleanField(default=False)
    enable_csrf = models.BooleanField(default=True)
    allowed_hosts = models.TextField(default='*', help_text='Comma-separated list of allowed hosts')
    
    # Email Configuration
    smtp_host = models.CharField(max_length=100, default='smtp.gmail.com')
    smtp_port = models.IntegerField(default=587)
    smtp_username = models.EmailField(blank=True)
    smtp_password = models.CharField(max_length=255, blank=True)
    from_email = models.EmailField(default='noreply@farmazee.com')
    from_name = models.CharField(max_length=100, default='Farmazee')
    email_use_tls = models.BooleanField(default=True)
    email_use_ssl = models.BooleanField(default=False)
    
    # Notification Settings
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=False)
    admin_alerts = models.BooleanField(default=True)
    notification_email = models.EmailField(default='admin@farmazee.com')
    
    # Backup & Maintenance
    auto_backup = models.BooleanField(default=True)
    backup_frequency = models.CharField(max_length=20, choices=[
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ], default='daily')
    retain_backups = models.IntegerField(default=30)  # days
    backup_location = models.CharField(max_length=255, default='/backups')
    last_backup = models.DateTimeField(null=True, blank=True)
    
    # Integrations
    openrouter_api_key = models.CharField(max_length=255, blank=True)
    weather_api_key = models.CharField(max_length=255, blank=True)
    google_maps_api_key = models.CharField(max_length=255, blank=True)
    payment_gateway = models.CharField(max_length=50, choices=[
        ('razorpay', 'Razorpay'),
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal')
    ], default='razorpay')
    
    # UI/UX Customization
    primary_color = models.CharField(max_length=7, default='#007bff')
    secondary_color = models.CharField(max_length=7, default='#6c757d')
    accent_color = models.CharField(max_length=7, default='#28a745')
    font_family = models.CharField(max_length=100, default='Inter, sans-serif')
    enable_dark_mode = models.BooleanField(default=False)
    default_theme = models.CharField(max_length=20, choices=[
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto')
    ], default='light')
    
    # Content Customization
    homepage_title = models.CharField(max_length=200, default='Welcome to Farmazee')
    homepage_subtitle = models.TextField(default='Your smart farming companion')
    about_page_content = models.TextField(blank=True)
    contact_page_content = models.TextField(blank=True)
    footer_text = models.TextField(default='© 2024 Farmazee. All rights reserved.')
    
    # Feature Toggles
    enable_marketplace = models.BooleanField(default=True)
    enable_community = models.BooleanField(default=True)
    enable_ai_chatbot = models.BooleanField(default=True)
    enable_weather = models.BooleanField(default=True)
    enable_soil_health = models.BooleanField(default=True)
    enable_crop_planning = models.BooleanField(default=True)
    enable_schemes = models.BooleanField(default=True)
    
    # SEO Settings
    meta_title = models.CharField(max_length=60, default='Farmazee - Smart Farming Solutions')
    meta_description = models.TextField(default='Farmazee provides smart farming solutions, crop advice, and agricultural tools for modern farmers.')
    meta_keywords = models.TextField(blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    facebook_pixel_id = models.CharField(max_length=50, blank=True)
    
    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # Legal Pages
    terms_of_service = models.TextField(blank=True)
    privacy_policy = models.TextField(blank=True)
    cookie_policy = models.TextField(blank=True)
    
    # Performance Settings
    enable_caching = models.BooleanField(default=True)
    cache_timeout = models.IntegerField(default=300)  # seconds
    enable_compression = models.BooleanField(default=True)
    enable_minification = models.BooleanField(default=True)
    
    # Created/Updated
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'System Setting'
        verbose_name_plural = 'System Settings'
    
    def __str__(self):
        return f"System Settings - {self.site_name}"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SystemSettings.objects.exists():
            return
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create system settings singleton"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Farmazee',
                'site_description': 'Smart Farming Solutions'
            }
        )
        return settings

