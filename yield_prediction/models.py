from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class CropType(models.Model):
    """Model for different crop types with their characteristics"""
    
    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=50, choices=[
        ('cereal', 'Cereal'),
        ('pulse', 'Pulse'),
        ('oilseed', 'Oilseed'),
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
        ('spice', 'Spice'),
        ('fiber', 'Fiber'),
        ('other', 'Other'),
    ])
    description = models.TextField(blank=True)
    
    # Yield characteristics (per hectare)
    base_yield_min = models.FloatField(help_text="Minimum expected yield (quintals/hectare)")
    base_yield_max = models.FloatField(help_text="Maximum expected yield (quintals/hectare)")
    average_yield = models.FloatField(help_text="Average expected yield (quintals/hectare)")
    
    # Growth requirements
    growing_season = models.CharField(max_length=50, choices=[
        ('kharif', 'Kharif (Monsoon)'),
        ('rabi', 'Rabi (Winter)'),
        ('zaid', 'Zaid (Summer)'),
        ('year_round', 'Year Round'),
    ])
    maturity_days = models.PositiveIntegerField(help_text="Days to maturity")
    water_requirement = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    
    # Soil preferences
    preferred_soil_types = models.CharField(max_length=200, blank=True, help_text="Comma-separated soil types")
    ph_range_min = models.FloatField(default=6.0)
    ph_range_max = models.FloatField(default=7.5)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Crop Type"
        verbose_name_plural = "Crop Types"
    
    def __str__(self):
        return self.name


class SoilType(models.Model):
    """Model for different soil types with their characteristics"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    # Soil characteristics
    fertility_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    water_retention = models.CharField(max_length=20, choices=[
        ('poor', 'Poor'),
        ('good', 'Good'),
        ('excellent', 'Excellent'),
    ])
    drainage = models.CharField(max_length=20, choices=[
        ('poor', 'Poor'),
        ('good', 'Good'),
        ('excellent', 'Excellent'),
    ])
    
    # Yield impact factors
    yield_multiplier = models.FloatField(default=1.0, help_text="Multiplier for yield calculation")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = "Soil Type"
        verbose_name_plural = "Soil Types"
    
    def __str__(self):
        return self.name


class YieldPrediction(models.Model):
    """Model for storing yield predictions made by farmers"""
    
    SEASON_CHOICES = [
        ('kharif', 'Kharif (Monsoon)'),
        ('rabi', 'Rabi (Winter)'),
        ('zaid', 'Zaid (Summer)'),
        ('year_round', 'Year Round'),
    ]
    
    IRRIGATION_CHOICES = [
        ('rainfed', 'Rainfed'),
        ('irrigated', 'Irrigated'),
        ('drip', 'Drip Irrigation'),
        ('sprinkler', 'Sprinkler Irrigation'),
    ]
    
    FERTILIZER_CHOICES = [
        ('organic', 'Organic'),
        ('chemical', 'Chemical'),
        ('mixed', 'Mixed (Organic + Chemical)'),
        ('none', 'No Fertilizer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='yield_predictions')
    crop_type = models.ForeignKey(CropType, on_delete=models.CASCADE)
    soil_type = models.ForeignKey(SoilType, on_delete=models.CASCADE)
    
    # Farm details
    area_hectares = models.FloatField(validators=[MinValueValidator(0.1)], help_text="Area in hectares")
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    irrigation_type = models.CharField(max_length=20, choices=IRRIGATION_CHOICES)
    fertilizer_type = models.CharField(max_length=20, choices=FERTILIZER_CHOICES)
    
    # Prediction results
    predicted_yield_min = models.FloatField(help_text="Minimum predicted yield (quintals)")
    predicted_yield_max = models.FloatField(help_text="Maximum predicted yield (quintals)")
    predicted_yield_avg = models.FloatField(help_text="Average predicted yield (quintals)")
    confidence_level = models.CharField(max_length=20, choices=[
        ('low', 'Low (60-70%)'),
        ('medium', 'Medium (70-80%)'),
        ('high', 'High (80-90%)'),
        ('very_high', 'Very High (90%+)'),
    ])
    
    # Additional factors
    weather_condition = models.CharField(max_length=50, blank=True, help_text="Expected weather conditions")
    pest_disease_risk = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], default='medium')
    
    # Notes and recommendations
    notes = models.TextField(blank=True, help_text="Additional notes or recommendations")
    recommendations = models.TextField(blank=True, help_text="System-generated recommendations")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Yield Prediction"
        verbose_name_plural = "Yield Predictions"
    
    def __str__(self):
        return f"{self.crop_type.name} - {self.area_hectares} hectares - {self.predicted_yield_avg} quintals"
    
    @property
    def yield_per_hectare(self):
        """Calculate yield per hectare"""
        return self.predicted_yield_avg / self.area_hectares if self.area_hectares > 0 else 0
    
    @property
    def estimated_revenue(self):
        """Calculate estimated revenue (assuming average market price)"""
        # This would need market price data
        return self.predicted_yield_avg * 2000  # Assuming ₹2000 per quintal average


class YieldHistory(models.Model):
    """Model for storing actual yield data for future predictions"""
    
    prediction = models.ForeignKey(YieldPrediction, on_delete=models.CASCADE, related_name='history')
    actual_yield = models.FloatField(help_text="Actual yield achieved (quintals)")
    harvest_date = models.DateField()
    weather_conditions = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-harvest_date']
        verbose_name = "Yield History"
        verbose_name_plural = "Yield Histories"
    
    def __str__(self):
        return f"{self.prediction.crop_type.name} - {self.actual_yield} quintals on {self.harvest_date}"


class CropRecommendation(models.Model):
    """Model for crop recommendations based on soil and season"""
    
    soil_type = models.ForeignKey(SoilType, on_delete=models.CASCADE)
    season = models.CharField(max_length=20, choices=YieldPrediction.SEASON_CHOICES)
    recommended_crops = models.ManyToManyField(CropType, help_text="Crops suitable for this soil and season")
    description = models.TextField(help_text="Why these crops are recommended")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['soil_type', 'season']
        verbose_name = "Crop Recommendation"
        verbose_name_plural = "Crop Recommendations"
        unique_together = ['soil_type', 'season']
    
    def __str__(self):
        return f"{self.soil_type.name} - {self.get_season_display()}"