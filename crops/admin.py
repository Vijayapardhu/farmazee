from django.contrib import admin
from .models import (
    Crop, CropImage, CropPlan, CropActivity, CropMonitoring,
    PestDisease, PestDiseaseReport, YieldRecord, CropCalendar, CropAdvice
)

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'season', 'min_temperature', 'max_temperature', 'is_featured', 'created_at']
    list_filter = ['category', 'season', 'is_featured', 'created_at']
    search_fields = ['name', 'description', 'care_instructions']
    list_editable = ['is_featured']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'scientific_name', 'description', 'category', 'season', 'image')
        }),
        ('Growing Requirements', {
            'fields': ('min_temperature', 'max_temperature', 'rainfall_requirement', 'soil_type', 'ph_range')
        }),
        ('Growing Details', {
            'fields': ('sowing_time', 'harvesting_time', 'growth_duration', 'yield_per_acre')
        }),
        ('Care Instructions', {
            'fields': ('watering_needs', 'sunlight_requirements', 'care_instructions', 'harvesting_tips')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    list_per_page = 25

@admin.register(CropImage)
class CropImageAdmin(admin.ModelAdmin):
    list_display = ['crop', 'order', 'is_primary', 'alt_text']
    list_filter = ['is_primary', 'order']
    search_fields = ['crop__name', 'alt_text']
    list_editable = ['order', 'is_primary']

# Crop Management Admin
@admin.register(CropPlan)
class CropPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'crop', 'land_area', 'planned_sowing_date', 'expected_harvest_date', 'status']
    list_filter = ['status', 'crop__category', 'planned_sowing_date', 'created_at']
    search_fields = ['title', 'user__username', 'crop__name']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Plan Information', {
            'fields': ('user', 'title', 'description', 'crop')
        }),
        ('Land & Timing', {
            'fields': ('land_area', 'planned_sowing_date', 'expected_harvest_date')
        }),
        ('Financial', {
            'fields': ('budget',)
        }),
        ('Status & Notes', {
            'fields': ('status', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CropActivity)
class CropActivityAdmin(admin.ModelAdmin):
    list_display = ['crop_plan', 'activity_type', 'title', 'scheduled_date', 'is_completed', 'cost']
    list_filter = ['activity_type', 'is_completed', 'scheduled_date', 'created_at']
    search_fields = ['title', 'crop_plan__title', 'crop_plan__user__username']
    list_editable = ['is_completed']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('crop_plan', 'activity_type', 'title', 'description')
        }),
        ('Scheduling', {
            'fields': ('scheduled_date', 'completed_date', 'is_completed')
        }),
        ('Financial', {
            'fields': ('cost',)
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(CropMonitoring)
class CropMonitoringAdmin(admin.ModelAdmin):
    list_display = ['crop_plan', 'monitoring_date', 'growth_stage', 'health_status', 'height']
    list_filter = ['health_status', 'monitoring_date', 'created_at']
    search_fields = ['crop_plan__title', 'growth_stage', 'observations']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Monitoring Information', {
            'fields': ('crop_plan', 'monitoring_date', 'growth_stage', 'health_status', 'height')
        }),
        ('Observations', {
            'fields': ('observations', 'issues_found', 'recommendations')
        }),
        ('Media', {
            'fields': ('images',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(PestDisease)
class PestDiseaseAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'severity', 'is_active', 'created_at']
    list_filter = ['type', 'severity', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'symptoms']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'type', 'description', 'symptoms', 'severity')
        }),
        ('Treatment & Prevention', {
            'fields': ('treatment_methods', 'prevention_methods')
        }),
        ('Affected Crops', {
            'fields': ('affected_crops',)
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(PestDiseaseReport)
class PestDiseaseReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'crop_plan', 'pest_disease', 'report_date', 'severity', 'status']
    list_filter = ['severity', 'status', 'report_date', 'created_at']
    search_fields = ['user__username', 'pest_disease__name', 'description']
    list_editable = ['status']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Report Information', {
            'fields': ('user', 'crop_plan', 'pest_disease', 'report_date', 'description', 'severity')
        }),
        ('Impact Assessment', {
            'fields': ('affected_area',)
        }),
        ('Treatment & Resolution', {
            'fields': ('treatment_applied', 'resolution_date')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Media', {
            'fields': ('images',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(YieldRecord)
class YieldRecordAdmin(admin.ModelAdmin):
    list_display = ['crop_plan', 'harvest_date', 'quantity_harvested', 'quality_grade', 'market_price', 'total_value']
    list_filter = ['harvest_date', 'quality_grade', 'created_at']
    search_fields = ['crop_plan__title', 'crop_plan__user__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Harvest Information', {
            'fields': ('crop_plan', 'harvest_date', 'quantity_harvested', 'quality_grade')
        }),
        ('Market Information', {
            'fields': ('market_price', 'total_value')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(CropCalendar)
class CropCalendarAdmin(admin.ModelAdmin):
    list_display = ['crop', 'title', 'event_date', 'event_type', 'is_recurring']
    list_filter = ['event_type', 'is_recurring', 'event_date', 'created_at']
    search_fields = ['crop__name', 'title', 'description']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('crop', 'title', 'description', 'event_date', 'event_type')
        }),
        ('Recurrence', {
            'fields': ('is_recurring', 'recurrence_pattern')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(CropAdvice)
class CropAdviceAdmin(admin.ModelAdmin):
    list_display = ['crop', 'title', 'advice_type', 'season', 'is_featured', 'is_active']
    list_filter = ['advice_type', 'season', 'is_featured', 'is_active', 'created_at']
    search_fields = ['crop__name', 'title', 'content']
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Advice Information', {
            'fields': ('crop', 'title', 'content', 'advice_type', 'season')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
