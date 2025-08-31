from django.contrib import admin
from .models import (
    WeatherData, WeatherForecast, WeatherAlert,
    SoilMoistureData, AirQualityData, RainfallData, ClimateData,
    WeatherStation, WeatherSubscription, WeatherReport, SeasonalForecast
)

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'temperature', 'humidity', 'description', 'is_current', 'recorded_at']
    list_filter = ['is_current', 'recorded_at']
    search_fields = ['location', 'description']
    readonly_fields = ['recorded_at', 'updated_at']
    list_editable = ['is_current']
    
    fieldsets = (
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Weather Information', {
            'fields': ('temperature', 'humidity', 'description', 'wind_speed', 'wind_direction', 'pressure')
        }),
        ('Additional Data', {
            'fields': ('icon', 'visibility', 'uv_index')
        }),
        ('Status', {
            'fields': ('is_current',)
        }),
        ('Timestamps', {
            'fields': ('recorded_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(WeatherForecast)
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display = ['location', 'date', 'min_temperature', 'max_temperature', 'humidity', 'description']
    list_filter = ['date', 'created_at']
    search_fields = ['location', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Location & Date', {
            'fields': ('location', 'date')
        }),
        ('Temperature', {
            'fields': ('min_temperature', 'max_temperature')
        }),
        ('Weather Conditions', {
            'fields': ('humidity', 'wind_speed', 'wind_direction', 'description', 'icon')
        }),
        ('Precipitation', {
            'fields': ('precipitation_probability',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ['location', 'alert_type', 'severity', 'title', 'start_time', 'end_time', 'is_active']
    list_filter = ['alert_type', 'severity', 'is_active', 'start_time', 'created_at']
    search_fields = ['location', 'title', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('location', 'alert_type', 'severity', 'title', 'description')
        }),
        ('Timing', {
            'fields': ('start_time', 'end_time')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

# Environmental Monitoring Admin
@admin.register(SoilMoistureData)
class SoilMoistureDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'soil_moisture', 'soil_temperature', 'depth', 'recorded_at']
    list_filter = ['depth', 'recorded_at']
    search_fields = ['location']
    readonly_fields = ['recorded_at']
    
    fieldsets = (
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Soil Data', {
            'fields': ('soil_moisture', 'soil_temperature', 'depth')
        }),
        ('Timestamps', {
            'fields': ('recorded_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(AirQualityData)
class AirQualityDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'aqi', 'pm25', 'pm10', 'co', 'no2', 'o3', 'recorded_at']
    list_filter = ['recorded_at']
    search_fields = ['location']
    readonly_fields = ['recorded_at']
    
    fieldsets = (
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Air Quality Index', {
            'fields': ('aqi',)
        }),
        ('Particulate Matter', {
            'fields': ('pm25', 'pm10')
        }),
        ('Gases', {
            'fields': ('co', 'no2', 'o3')
        }),
        ('Timestamps', {
            'fields': ('recorded_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(RainfallData)
class RainfallDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'rainfall_amount', 'duration', 'intensity', 'recorded_at']
    list_filter = ['intensity', 'recorded_at']
    search_fields = ['location']
    readonly_fields = ['recorded_at']
    
    fieldsets = (
        ('Location', {
            'fields': ('location', 'latitude', 'longitude')
        }),
        ('Rainfall Data', {
            'fields': ('rainfall_amount', 'duration', 'intensity')
        }),
        ('Timestamps', {
            'fields': ('recorded_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(ClimateData)
class ClimateDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'year', 'month', 'avg_temperature', 'total_rainfall', 'rainy_days', 'humidity']
    list_filter = ['year', 'month', 'created_at']
    search_fields = ['location']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Location & Period', {
            'fields': ('location', 'year', 'month')
        }),
        ('Temperature Data', {
            'fields': ('avg_temperature', 'max_temperature', 'min_temperature')
        }),
        ('Rainfall Data', {
            'fields': ('total_rainfall', 'rainy_days')
        }),
        ('Other Data', {
            'fields': ('humidity',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(WeatherStation)
class WeatherStationAdmin(admin.ModelAdmin):
    list_display = ['name', 'station_type', 'location', 'elevation', 'is_active']
    list_filter = ['station_type', 'is_active', 'installation_date', 'created_at']
    search_fields = ['name', 'location', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Station Information', {
            'fields': ('name', 'station_type', 'description')
        }),
        ('Location', {
            'fields': ('location', 'latitude', 'longitude', 'elevation')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Maintenance', {
            'fields': ('installation_date', 'last_maintenance')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(WeatherSubscription)
class WeatherSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'notification_method', 'is_active', 'created_at']
    list_filter = ['notification_method', 'is_active', 'created_at']
    search_fields = ['user__username', 'location']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(WeatherReport)
class WeatherReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'report_date', 'weather_condition', 'temperature', 'humidity']
    list_filter = ['report_date', 'created_at']
    search_fields = ['user__username', 'location', 'weather_condition']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('user', 'location', 'report_date', 'weather_condition')
        }),
        ('Weather Data', {
            'fields': ('temperature', 'humidity', 'rainfall', 'wind_speed')
        }),
        ('Observations', {
            'fields': ('observations', 'impact_on_farming')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SeasonalForecast)
class SeasonalForecastAdmin(admin.ModelAdmin):
    list_display = ['location', 'season', 'year', 'confidence_level', 'created_at']
    list_filter = ['season', 'year', 'confidence_level', 'created_at']
    search_fields = ['location', 'forecast_period']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Forecast Information', {
            'fields': ('location', 'season', 'year', 'forecast_period')
        }),
        ('Outlook', {
            'fields': ('temperature_outlook', 'rainfall_outlook', 'humidity_outlook')
        }),
        ('Recommendations', {
            'fields': ('farming_recommendations',)
        }),
        ('Confidence', {
            'fields': ('confidence_level',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
