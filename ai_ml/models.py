"""
Advanced AI/ML Models for Farmazee Enterprise Platform.

This module contains models for machine learning predictions,
computer vision analysis, and intelligent recommendations.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords
import uuid

User = get_user_model()


class AIModel(models.Model):
    """Base model for AI/ML models."""
    
    MODEL_TYPES = [
        ('crop_prediction', 'Crop Prediction'),
        ('disease_detection', 'Disease Detection'),
        ('yield_forecast', 'Yield Forecast'),
        ('weather_prediction', 'Weather Prediction'),
        ('market_prediction', 'Market Prediction'),
        ('soil_analysis', 'Soil Analysis'),
        ('pest_detection', 'Pest Detection'),
        ('irrigation_optimization', 'Irrigation Optimization'),
    ]
    
    STATUS_CHOICES = [
        ('training', 'Training'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('error', 'Error'),
        ('deprecated', 'Deprecated'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    model_type = models.CharField(max_length=50, choices=MODEL_TYPES)
    version = models.CharField(max_length=20)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    
    # Model files
    model_file = models.FileField(upload_to='ai_models/', null=True, blank=True)
    weights_file = models.FileField(upload_to='ai_models/weights/', null=True, blank=True)
    config_file = models.JSONField(default=dict)
    
    # Performance metrics
    accuracy = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], null=True, blank=True)
    precision = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], null=True, blank=True)
    recall = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], null=True, blank=True)
    f1_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], null=True, blank=True)
    
    # Training information
    training_data_size = models.PositiveIntegerField(default=0)
    training_duration = models.DurationField(null=True, blank=True)
    last_trained = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_models')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # History tracking
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'AI Model'
        verbose_name_plural = 'AI Models'
    
    def __str__(self):
        return f"{self.name} v{self.version} ({self.get_model_type_display()})"


class Prediction(models.Model):
    """Model for storing AI/ML predictions."""
    
    PREDICTION_TYPES = [
        ('crop_yield', 'Crop Yield'),
        ('disease_risk', 'Disease Risk'),
        ('pest_infestation', 'Pest Infestation'),
        ('weather_forecast', 'Weather Forecast'),
        ('market_price', 'Market Price'),
        ('soil_health', 'Soil Health'),
        ('irrigation_schedule', 'Irrigation Schedule'),
        ('fertilizer_recommendation', 'Fertilizer Recommendation'),
    ]
    
    CONFIDENCE_LEVELS = [
        ('low', 'Low (< 60%)'),
        ('medium', 'Medium (60-80%)'),
        ('high', 'High (80-95%)'),
        ('very_high', 'Very High (> 95%)'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='predictions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    
    prediction_type = models.CharField(max_length=50, choices=PREDICTION_TYPES)
    input_data = models.JSONField(help_text='Input data used for prediction')
    prediction_result = models.JSONField(help_text='Prediction output')
    confidence_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    confidence_level = models.CharField(max_length=20, choices=CONFIDENCE_LEVELS)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # History tracking
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'
    
    def __str__(self):
        return f"{self.get_prediction_type_display()} - {self.user.username} ({self.confidence_score:.2%})"


class ComputerVisionAnalysis(models.Model):
    """Model for computer vision analysis results."""
    
    ANALYSIS_TYPES = [
        ('crop_health', 'Crop Health'),
        ('disease_detection', 'Disease Detection'),
        ('pest_detection', 'Pest Detection'),
        ('growth_stage', 'Growth Stage'),
        ('weed_detection', 'Weed Detection'),
        ('soil_analysis', 'Soil Analysis'),
        ('equipment_detection', 'Equipment Detection'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cv_analyses')
    analysis_type = models.CharField(max_length=50, choices=ANALYSIS_TYPES)
    
    # Image data
    image = models.ImageField(upload_to='cv_analysis/')
    thumbnail = models.ImageField(upload_to='cv_analysis/thumbnails/', null=True, blank=True)
    
    # Analysis results
    analysis_result = models.JSONField(help_text='Computer vision analysis results')
    detected_objects = models.JSONField(default=list, help_text='List of detected objects')
    confidence_scores = models.JSONField(default=dict, help_text='Confidence scores for detections')
    
    # Processing metadata
    processing_time = models.FloatField(help_text='Processing time in seconds')
    model_version = models.CharField(max_length=20, help_text='AI model version used')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    # History tracking
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Computer Vision Analysis'
        verbose_name_plural = 'Computer Vision Analyses'
    
    def __str__(self):
        return f"{self.get_analysis_type_display()} - {self.user.username} ({self.created_at.strftime('%Y-%m-%d')})"


class Recommendation(models.Model):
    """Model for AI-generated recommendations."""
    
    RECOMMENDATION_TYPES = [
        ('crop_selection', 'Crop Selection'),
        ('planting_time', 'Planting Time'),
        ('irrigation_schedule', 'Irrigation Schedule'),
        ('fertilizer_application', 'Fertilizer Application'),
        ('pest_control', 'Pest Control'),
        ('disease_prevention', 'Disease Prevention'),
        ('harvest_timing', 'Harvest Timing'),
        ('market_timing', 'Market Timing'),
        ('equipment_usage', 'Equipment Usage'),
        ('resource_allocation', 'Resource Allocation'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommendation_type = models.CharField(max_length=50, choices=RECOMMENDATION_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    
    # Recommendation content
    title = models.CharField(max_length=200)
    description = models.TextField()
    action_items = models.JSONField(default=list, help_text='List of specific actions to take')
    expected_benefits = models.TextField(help_text='Expected benefits of following the recommendation')
    
    # AI metadata
    confidence_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)])
    reasoning = models.TextField(help_text='AI reasoning behind the recommendation')
    supporting_data = models.JSONField(default=dict, help_text='Supporting data and evidence')
    
    # User interaction
    is_read = models.BooleanField(default=False)
    is_applied = models.BooleanField(default=False)
    applied_at = models.DateTimeField(null=True, blank=True)
    feedback_rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    feedback_comment = models.TextField(blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    
    # History tracking
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-priority', '-created_at']
        verbose_name = 'Recommendation'
        verbose_name_plural = 'Recommendations'
    
    def __str__(self):
        return f"{self.title} - {self.user.username} ({self.get_priority_display()})"


class TrainingJob(models.Model):
    """Model for tracking AI model training jobs."""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    model = models.ForeignKey(AIModel, on_delete=models.CASCADE, related_name='training_jobs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='training_jobs')
    
    # Job configuration
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    training_config = models.JSONField(help_text='Training configuration parameters')
    dataset_info = models.JSONField(help_text='Information about the training dataset')
    
    # Progress tracking
    progress_percentage = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    current_epoch = models.PositiveIntegerField(default=0)
    total_epochs = models.PositiveIntegerField()
    
    # Performance metrics
    training_loss = models.FloatField(null=True, blank=True)
    validation_loss = models.FloatField(null=True, blank=True)
    training_accuracy = models.FloatField(null=True, blank=True)
    validation_accuracy = models.FloatField(null=True, blank=True)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    
    # Logs and artifacts
    training_logs = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    artifacts_path = models.CharField(max_length=500, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # History tracking
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Training Job'
        verbose_name_plural = 'Training Jobs'
    
    def __str__(self):
        return f"Training {self.model.name} - {self.get_status_display()} ({self.progress_percentage:.1f}%)"


class DataSource(models.Model):
    """Model for tracking data sources used in AI/ML."""
    
    SOURCE_TYPES = [
        ('satellite', 'Satellite Imagery'),
        ('drone', 'Drone Imagery'),
        ('sensor', 'IoT Sensors'),
        ('weather_station', 'Weather Station'),
        ('market_data', 'Market Data'),
        ('soil_lab', 'Soil Laboratory'),
        ('manual_input', 'Manual Input'),
        ('api', 'External API'),
        ('database', 'Database'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    source_type = models.CharField(max_length=50, choices=SOURCE_TYPES)
    description = models.TextField()
    
    # Data characteristics
    data_format = models.CharField(max_length=50)
    update_frequency = models.CharField(max_length=100, help_text='How often data is updated')
    data_quality_score = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(1.0)], null=True, blank=True)
    
    # Access information
    access_url = models.URLField(blank=True)
    api_key_required = models.BooleanField(default=False)
    rate_limit = models.CharField(max_length=100, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    # History tracking
    history = HistoricalRecords()
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Data Source'
        verbose_name_plural = 'Data Sources'
    
    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"

