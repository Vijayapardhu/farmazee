from django.contrib import admin
from .models import CropType, SoilType, YieldPrediction, YieldHistory, CropRecommendation

@admin.register(CropType)
class CropTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'average_yield', 'growing_season', 'maturity_days', 'is_active']
    list_filter = ['category', 'growing_season', 'water_requirement', 'is_active']
    search_fields = ['name', 'scientific_name', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'scientific_name', 'category', 'description', 'is_active')
        }),
        ('Yield Characteristics', {
            'fields': ('base_yield_min', 'base_yield_max', 'average_yield')
        }),
        ('Growth Requirements', {
            'fields': ('growing_season', 'maturity_days', 'water_requirement')
        }),
        ('Soil Preferences', {
            'fields': ('preferred_soil_types', 'ph_range_min', 'ph_range_max')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(SoilType)
class SoilTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'fertility_level', 'water_retention', 'drainage', 'yield_multiplier', 'is_active']
    list_filter = ['fertility_level', 'water_retention', 'drainage', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'is_active')
        }),
        ('Soil Characteristics', {
            'fields': ('fertility_level', 'water_retention', 'drainage')
        }),
        ('Yield Impact', {
            'fields': ('yield_multiplier',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(YieldPrediction)
class YieldPredictionAdmin(admin.ModelAdmin):
    list_display = ['crop_type', 'user', 'area_hectares', 'predicted_yield_avg', 'confidence_level', 'created_at']
    list_filter = ['season', 'irrigation_type', 'fertilizer_type', 'confidence_level', 'created_at']
    search_fields = ['crop_type__name', 'user__username', 'soil_type__name', 'notes']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'crop_type', 'soil_type', 'area_hectares')
        }),
        ('Farming Conditions', {
            'fields': ('season', 'irrigation_type', 'fertilizer_type', 'weather_condition', 'pest_disease_risk')
        }),
        ('Prediction Results', {
            'fields': ('predicted_yield_min', 'predicted_yield_max', 'predicted_yield_avg', 'confidence_level')
        }),
        ('Notes & Recommendations', {
            'fields': ('notes', 'recommendations')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(YieldHistory)
class YieldHistoryAdmin(admin.ModelAdmin):
    list_display = ['prediction', 'actual_yield', 'harvest_date', 'weather_conditions']
    list_filter = ['harvest_date', 'prediction__crop_type']
    search_fields = ['prediction__crop_type__name', 'weather_conditions', 'notes']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Harvest Information', {
            'fields': ('prediction', 'actual_yield', 'harvest_date')
        }),
        ('Conditions', {
            'fields': ('weather_conditions', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )

@admin.register(CropRecommendation)
class CropRecommendationAdmin(admin.ModelAdmin):
    list_display = ['soil_type', 'season', 'recommended_crops_count', 'is_active']
    list_filter = ['season', 'is_active', 'soil_type']
    search_fields = ['soil_type__name', 'description']
    readonly_fields = ['created_at']
    filter_horizontal = ['recommended_crops']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('soil_type', 'season', 'description', 'is_active')
        }),
        ('Recommended Crops', {
            'fields': ('recommended_crops',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
    
    def recommended_crops_count(self, obj):
        return obj.recommended_crops.count()
    recommended_crops_count.short_description = 'Number of Crops'