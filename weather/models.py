from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class WeatherData(models.Model):
    """Weather data model"""
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text='Temperature in Celsius')
    humidity = models.IntegerField(help_text='Humidity percentage')
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, help_text='Wind speed in km/h')
    wind_direction = models.CharField(max_length=10, blank=True, null=True)
    pressure = models.DecimalField(max_digits=6, decimal_places=2, help_text='Pressure in hPa')
    description = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True)
    visibility = models.DecimalField(max_digits=5, decimal_places=2, help_text='Visibility in km')
    uv_index = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    is_current = models.BooleanField(default=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Weather Data')
        verbose_name_plural = _('Weather Data')
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"{self.location} - {self.temperature}°C - {self.description}"


class WeatherForecast(models.Model):
    """Weather forecast model"""
    location = models.CharField(max_length=200)
    date = models.DateField()
    min_temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text='Minimum temperature in Celsius')
    max_temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text='Maximum temperature in Celsius')
    humidity = models.IntegerField(help_text='Humidity percentage')
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, help_text='Wind speed in km/h')
    wind_direction = models.CharField(max_length=10, blank=True, null=True)
    description = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, null=True)
    precipitation_probability = models.IntegerField(help_text='Precipitation probability percentage', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Weather Forecast')
        verbose_name_plural = _('Weather Forecasts')
        ordering = ['date']
        unique_together = ['location', 'date']
    
    def __str__(self):
        return f"{self.location} - {self.date} - {self.min_temperature}°C to {self.max_temperature}°C"


class WeatherAlert(models.Model):
    """Weather alert model"""
    ALERT_TYPES = [
        ('storm', 'Storm Warning'),
        ('heavy_rain', 'Heavy Rain'),
        ('drought', 'Drought Warning'),
        ('heat_wave', 'Heat Wave'),
        ('cold_wave', 'Cold Wave'),
        ('flood', 'Flood Warning'),
        ('cyclone', 'Cyclone Warning'),
        ('other', 'Other'),
    ]
    
    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    location = models.CharField(max_length=200)
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS)
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.location} - {self.get_alert_type_display()} - {self.get_severity_display()}"


# Environmental Monitoring Models
class SoilMoistureData(models.Model):
    """Soil moisture monitoring data"""
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    soil_moisture = models.DecimalField(max_digits=4, decimal_places=2, help_text='Soil moisture percentage')
    soil_temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text='Soil temperature in Celsius')
    depth = models.DecimalField(max_digits=3, decimal_places=1, help_text='Depth in cm')
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"{self.location} - {self.soil_moisture}% moisture at {self.depth}cm"


class AirQualityData(models.Model):
    """Air quality monitoring data"""
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    aqi = models.IntegerField(help_text='Air Quality Index')
    pm25 = models.DecimalField(max_digits=5, decimal_places=2, help_text='PM2.5 concentration')
    pm10 = models.DecimalField(max_digits=5, decimal_places=2, help_text='PM10 concentration')
    co = models.DecimalField(max_digits=5, decimal_places=2, help_text='Carbon monoxide concentration')
    no2 = models.DecimalField(max_digits=5, decimal_places=2, help_text='Nitrogen dioxide concentration')
    o3 = models.DecimalField(max_digits=5, decimal_places=2, help_text='Ozone concentration')
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"{self.location} - AQI: {self.aqi}"


class RainfallData(models.Model):
    """Rainfall monitoring data"""
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    rainfall_amount = models.DecimalField(max_digits=6, decimal_places=2, help_text='Rainfall in mm')
    duration = models.IntegerField(help_text='Duration in minutes')
    intensity = models.CharField(max_length=20, blank=True, null=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recorded_at']
    
    def __str__(self):
        return f"{self.location} - {self.rainfall_amount}mm in {self.duration}min"


class ClimateData(models.Model):
    """Historical climate data"""
    location = models.CharField(max_length=200)
    year = models.IntegerField()
    month = models.IntegerField()
    avg_temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text='Average temperature in Celsius')
    max_temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text='Maximum temperature in Celsius')
    min_temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text='Minimum temperature in Celsius')
    total_rainfall = models.DecimalField(max_digits=6, decimal_places=2, help_text='Total rainfall in mm')
    rainy_days = models.IntegerField(help_text='Number of rainy days')
    humidity = models.DecimalField(max_digits=4, decimal_places=1, help_text='Average humidity percentage')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['location', 'year', 'month']
    
    def __str__(self):
        return f"{self.location} - {self.year}/{self.month} - {self.avg_temperature}°C"


class WeatherStation(models.Model):
    """Weather station information"""
    STATION_TYPES = [
        ('automatic', 'Automatic Weather Station'),
        ('manual', 'Manual Weather Station'),
        ('mobile', 'Mobile Weather Station'),
        ('satellite', 'Satellite Data'),
    ]
    
    name = models.CharField(max_length=200)
    station_type = models.CharField(max_length=20, choices=STATION_TYPES)
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    elevation = models.DecimalField(max_digits=6, decimal_places=2, help_text='Elevation in meters')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    installation_date = models.DateField(blank=True, null=True)
    last_maintenance = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.location}"


class WeatherSubscription(models.Model):
    """Weather alert subscriptions for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weather_subscriptions')
    location = models.CharField(max_length=200)
    alert_types = models.JSONField(default=list, help_text='List of alert types to subscribe to')
    notification_method = models.CharField(max_length=20, choices=[
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
        ('all', 'All'),
    ])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.location}"


class WeatherReport(models.Model):
    """Weather reports submitted by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weather_reports')
    location = models.CharField(max_length=200)
    report_date = models.DateField()
    weather_condition = models.CharField(max_length=100)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text='Temperature in Celsius')
    humidity = models.IntegerField(help_text='Humidity percentage')
    rainfall = models.DecimalField(max_digits=6, decimal_places=2, help_text='Rainfall in mm', blank=True, null=True)
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, help_text='Wind speed in km/h', blank=True, null=True)
    observations = models.TextField()
    impact_on_farming = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-report_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.location} - {self.report_date}"


class SeasonalForecast(models.Model):
    """Seasonal weather forecasts"""
    SEASONS = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('pre_monsoon', 'Pre-Monsoon'),
        ('post_monsoon', 'Post-Monsoon'),
    ]
    
    location = models.CharField(max_length=200)
    season = models.CharField(max_length=20, choices=SEASONS)
    year = models.IntegerField()
    forecast_period = models.CharField(max_length=100, help_text='Forecast period description')
    temperature_outlook = models.TextField()
    rainfall_outlook = models.TextField()
    humidity_outlook = models.TextField()
    confidence_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ])
    farming_recommendations = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-year', 'season']
        unique_together = ['location', 'season', 'year']
    
    def __str__(self):
        return f"{self.location} - {self.get_season_display()} {self.year}"

