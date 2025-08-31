from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
# from simple_history.models import HistoricalRecords


class Crop(models.Model):
    """Crop model for storing crop information"""
    CROP_CATEGORIES = [
        ('cereals', 'Cereals'),
        ('pulses', 'Pulses'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('oilseeds', 'Oilseeds'),
        ('cash_crops', 'Cash Crops'),
        ('spices', 'Spices'),
        ('medicinal', 'Medicinal Plants'),
        ('other', 'Other'),
    ]
    
    SEASONS = [
        ('kharif', 'Kharif'),
        ('rabi', 'Rabi'),
        ('zaid', 'Zaid'),
        ('all_season', 'All Season'),
    ]
    
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=20, choices=CROP_CATEGORIES)
    season = models.CharField(max_length=20, choices=SEASONS)
    description = models.TextField()
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    
    # Growing requirements
    min_temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text='Minimum temperature in Celsius')
    max_temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text='Maximum temperature in Celsius')
    rainfall_requirement = models.CharField(max_length=100, help_text='Rainfall requirement')
    soil_type = models.CharField(max_length=100, help_text='Preferred soil type')
    ph_range = models.CharField(max_length=50, help_text='Optimal pH range')
    
    # Growing details
    sowing_time = models.CharField(max_length=200, help_text='Best time for sowing')
    harvesting_time = models.CharField(max_length=200, help_text='Harvesting period')
    growth_duration = models.CharField(max_length=100, help_text='Days to maturity')
    yield_per_acre = models.CharField(max_length=100, help_text='Expected yield per acre')
    
    # Care instructions
    watering_needs = models.TextField(help_text='Watering requirements and schedule')
    sunlight_requirements = models.CharField(max_length=100, help_text='Sunlight requirements')
    care_instructions = models.TextField(help_text='General care instructions')
    harvesting_tips = models.TextField(help_text='Tips for harvesting')
    
    # Additional information
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Crop')
        verbose_name_plural = _('Crops')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CropImage(models.Model):
    """Crop images model"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='crops/')
    alt_text = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(default=0)
    is_primary = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.crop.name} - Image {self.order}"


# Crop Management Models
class CropPlan(models.Model):
    """Crop planning model"""
    PLAN_STATUS = [
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crop_plans')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    land_area = models.DecimalField(max_digits=8, decimal_places=2, help_text='Area in acres')
    planned_sowing_date = models.DateField()
    expected_harvest_date = models.DateField()
    status = models.CharField(max_length=20, choices=PLAN_STATUS, default='draft')
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.crop.name}"


class CropActivity(models.Model):
    """Crop activity tracking model"""
    ACTIVITY_TYPES = [
        ('sowing', 'Sowing'),
        ('irrigation', 'Irrigation'),
        ('fertilization', 'Fertilization'),
        ('pest_control', 'Pest Control'),
        ('weeding', 'Weeding'),
        ('harvesting', 'Harvesting'),
        ('post_harvest', 'Post Harvest'),
        ('other', 'Other'),
    ]
    
    crop_plan = models.ForeignKey(CropPlan, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    scheduled_date = models.DateField()
    completed_date = models.DateField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['scheduled_date']
        verbose_name_plural = 'Crop Activities'
    
    def __str__(self):
        return f"{self.title} - {self.get_activity_type_display()}"


class CropMonitoring(models.Model):
    """Crop monitoring and health tracking"""
    GROWTH_STAGES = [
        ('seedling', 'Seedling'),
        ('vegetative', 'Vegetative'),
        ('flowering', 'Flowering'),
        ('fruiting', 'Fruiting'),
        ('mature', 'Mature'),
        ('harvest_ready', 'Harvest Ready'),
    ]
    
    HEALTH_STATUS = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]
    
    crop_plan = models.ForeignKey(CropPlan, on_delete=models.CASCADE, related_name='monitoring_records')
    monitoring_date = models.DateField()
    growth_stage = models.CharField(max_length=20, choices=GROWTH_STAGES)
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='Height in cm')
    observations = models.TextField()
    issues_found = models.TextField(blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    images = models.ImageField(upload_to='crop_monitoring/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-monitoring_date']
    
    def __str__(self):
        return f"{self.crop_plan.crop.name} - {self.monitoring_date} - {self.get_health_status_display()}"


class PestDisease(models.Model):
    """Pest and disease information"""
    TYPE_CHOICES = [
        ('pest', 'Pest'),
        ('disease', 'Disease'),
        ('deficiency', 'Nutrient Deficiency'),
        ('other', 'Other'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    symptoms = models.TextField()
    affected_crops = models.ManyToManyField(Crop, related_name='pests_diseases')
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    treatment_methods = models.TextField()
    prevention_methods = models.TextField()
    image = models.ImageField(upload_to='pests_diseases/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Pests and Diseases'
    
    def __str__(self):
        return f"{self.name} - {self.get_type_display()}"


class PestDiseaseReport(models.Model):
    """Pest and disease reports from farmers"""
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('investigating', 'Investigating'),
        ('treated', 'Treated'),
        ('resolved', 'Resolved'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pest_reports')
    crop_plan = models.ForeignKey(CropPlan, on_delete=models.CASCADE, related_name='pest_reports')
    pest_disease = models.ForeignKey(PestDisease, on_delete=models.CASCADE)
    report_date = models.DateField()
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=PestDisease.SEVERITY_LEVELS)
    affected_area = models.DecimalField(max_digits=5, decimal_places=2, help_text='Affected area in acres')
    images = models.ImageField(upload_to='pest_reports/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    treatment_applied = models.TextField(blank=True, null=True)
    resolution_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-report_date']
    
    def __str__(self):
        return f"{self.pest_disease.name} - {self.crop_plan.crop.name} - {self.get_status_display()}"


class YieldRecord(models.Model):
    """Crop yield records"""
    crop_plan = models.ForeignKey(CropPlan, on_delete=models.CASCADE, related_name='yield_records')
    harvest_date = models.DateField()
    quantity_harvested = models.DecimalField(max_digits=8, decimal_places=2, help_text='Quantity in kg')
    quality_grade = models.CharField(max_length=20, blank=True, null=True)
    market_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text='Price per kg')
    total_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-harvest_date']
    
    def __str__(self):
        return f"{self.crop_plan.crop.name} - {self.harvest_date} - {self.quantity_harvested} kg"


class CropCalendar(models.Model):
    """Crop calendar for planning"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='calendar_events')
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateField()
    event_type = models.CharField(max_length=50)
    is_recurring = models.BooleanField(default=False)
    recurrence_pattern = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['event_date']
    
    def __str__(self):
        return f"{self.crop.name} - {self.title} - {self.event_date}"


class CropAdvice(models.Model):
    """Crop-specific advice and recommendations"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='advice')
    title = models.CharField(max_length=200)
    content = models.TextField()
    advice_type = models.CharField(max_length=50)
    season = models.CharField(max_length=20, choices=Crop.SEASONS, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.crop.name} - {self.title}"

