from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class SoilType(models.Model):
    """Soil type model"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = _('Soil Type')
        verbose_name_plural = _('Soil Types')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class SoilTip(models.Model):
    """Soil health tips model"""
    CATEGORIES = [
        ('testing', 'Soil Testing'),
        ('improvement', 'Soil Improvement'),
        ('conservation', 'Soil Conservation'),
        ('organic', 'Organic Methods'),
        ('nutrients', 'Nutrient Management'),
        ('erosion', 'Erosion Control'),
        ('general', 'General'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    content = models.TextField()
    image = models.ImageField(upload_to='soil_tips/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class SoilTest(models.Model):
    """Soil testing model"""
    TEST_TYPES = [
        ('ph', 'pH Test'),
        ('npk', 'NPK Test'),
        ('organic_matter', 'Organic Matter Test'),
        ('micronutrients', 'Micronutrients Test'),
        ('texture', 'Soil Texture Test'),
        ('salinity', 'Salinity Test'),
        ('comprehensive', 'Comprehensive Test'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='soil_tests')
    test_type = models.CharField(max_length=20, choices=TEST_TYPES)
    test_date = models.DateField()
    location = models.CharField(max_length=200)
    soil_depth = models.CharField(max_length=100, blank=True, null=True)
    sample_weight = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_test_type_display()} - {self.test_date}"


class SoilTestResult(models.Model):
    """Soil test results model"""
    PARAMETERS = [
        ('ph', 'pH Level'),
        ('nitrogen', 'Nitrogen (N)'),
        ('phosphorus', 'Phosphorus (P)'),
        ('potassium', 'Potassium (K)'),
        ('organic_matter', 'Organic Matter'),
        ('calcium', 'Calcium (Ca)'),
        ('magnesium', 'Magnesium (Mg)'),
        ('sulfur', 'Sulfur (S)'),
        ('zinc', 'Zinc (Zn)'),
        ('iron', 'Iron (Fe)'),
        ('manganese', 'Manganese (Mn)'),
        ('copper', 'Copper (Cu)'),
        ('boron', 'Boron (B)'),
        ('electrical_conductivity', 'Electrical Conductivity'),
    ]
    
    STATUS_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('optimal', 'Optimal'),
    ]
    
    soil_test = models.ForeignKey(SoilTest, on_delete=models.CASCADE, related_name='results')
    parameter = models.CharField(max_length=30, choices=PARAMETERS)
    value = models.DecimalField(max_digits=8, decimal_places=3)
    unit = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    recommendation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.parameter}: {self.value} {self.unit} - {self.soil_test}"


class SoilHealthRecord(models.Model):
    """Soil health monitoring records"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='soil_health_records')
    record_date = models.DateField()
    location = models.CharField(max_length=200)
    soil_type = models.ForeignKey(SoilType, on_delete=models.CASCADE, blank=True, null=True)
    
    # Basic properties
    ph_level = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    organic_matter = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text='Organic matter %')
    
    # Macronutrients
    nitrogen = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='N in kg/ha')
    phosphorus = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='P in kg/ha')
    potassium = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='K in kg/ha')
    
    # Secondary nutrients
    calcium = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='Ca in meq/100g')
    magnesium = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='Mg in meq/100g')
    sulfur = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='S in ppm')
    
    # Micronutrients
    micronutrients = models.TextField(blank=True, null=True, help_text='Other micronutrients data')
    
    # Health assessment
    is_healthy = models.BooleanField(default=True)
    health_score = models.IntegerField(choices=[(i, i) for i in range(1, 11)], blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-record_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.location} - {self.record_date}"


class FertilizerRecommendation(models.Model):
    """Fertilizer recommendation based on soil test results"""
    soil_test_result = models.ForeignKey(SoilTestResult, on_delete=models.CASCADE, related_name='fertilizer_recommendations')
    fertilizer_name = models.CharField(max_length=200)
    application_rate = models.CharField(max_length=100)
    application_method = models.CharField(max_length=100)
    recommendation = models.TextField()
    precautions = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.fertilizer_name} - {self.soil_test_result.parameter}"


class SoilImprovement(models.Model):
    """Soil improvement practices and methods"""
    IMPROVEMENT_TYPES = [
        ('organic_matter', 'Organic Matter Addition'),
        ('ph_adjustment', 'pH Adjustment'),
        ('drainage', 'Drainage Improvement'),
        ('erosion_control', 'Erosion Control'),
        ('compaction_relief', 'Compaction Relief'),
        ('nutrient_management', 'Nutrient Management'),
        ('crop_rotation', 'Crop Rotation'),
        ('cover_cropping', 'Cover Cropping'),
        ('mulching', 'Mulching'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    EFFECTIVENESS_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('excellent', 'Excellent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='soil_improvements')
    improvement_type = models.CharField(max_length=20, choices=IMPROVEMENT_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    progress_percentage = models.IntegerField(default=0, help_text='Progress percentage (0-100)')
    effectiveness = models.CharField(max_length=20, choices=EFFECTIVENESS_CHOICES, blank=True, null=True)
    results = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_improvement_type_display()} - {self.location}"


class SoilConservation(models.Model):
    """Soil conservation practices"""
    CONSERVATION_TYPES = [
        ('terracing', 'Terracing'),
        ('contour_plowing', 'Contour Plowing'),
        ('strip_cropping', 'Strip Cropping'),
        ('windbreaks', 'Windbreaks'),
        ('grassed_waterways', 'Grassed Waterways'),
        ('conservation_tillage', 'Conservation Tillage'),
        ('buffer_strips', 'Buffer Strips'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('implemented', 'Implemented'),
        ('maintained', 'Maintained'),
        ('abandoned', 'Abandoned'),
    ]
    
    EFFECTIVENESS_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('excellent', 'Excellent'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='soil_conservations')
    conservation_type = models.CharField(max_length=20, choices=CONSERVATION_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    implementation_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    funding_source = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    effectiveness = models.CharField(max_length=20, choices=EFFECTIVENESS_CHOICES, blank=True, null=True)
    monitoring_frequency = models.CharField(max_length=100, blank=True, null=True)
    last_monitoring_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_conservation_type_display()} - {self.location}"


class SoilMonitoringSchedule(models.Model):
    """Soil monitoring schedule for farmers"""
    MONITORING_TYPES = [
        ('ph', 'pH Monitoring'),
        ('nutrients', 'Nutrient Monitoring'),
        ('organic_matter', 'Organic Matter Monitoring'),
        ('erosion', 'Erosion Monitoring'),
        ('compaction', 'Compaction Monitoring'),
        ('comprehensive', 'Comprehensive Monitoring'),
    ]
    
    FREQUENCY_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('seasonally', 'Seasonally'),
        ('annually', 'Annually'),
        ('custom', 'Custom'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='soil_monitoring_schedules')
    monitoring_type = models.CharField(max_length=20, choices=MONITORING_TYPES)
    description = models.TextField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    next_monitoring_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['next_monitoring_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_monitoring_type_display()} - {self.next_monitoring_date}"


class SoilHealthAlert(models.Model):
    """Soil health alerts and notifications"""
    ALERT_TYPES = [
        ('degradation', 'Soil Degradation'),
        ('erosion', 'Erosion Risk'),
        ('nutrient_deficiency', 'Nutrient Deficiency'),
        ('ph_imbalance', 'pH Imbalance'),
        ('compaction', 'Soil Compaction'),
        ('salinity', 'Salinity Issues'),
        ('organic_matter', 'Low Organic Matter'),
        ('other', 'Other'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='soil_health_alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title} - {self.get_severity_display()}"

