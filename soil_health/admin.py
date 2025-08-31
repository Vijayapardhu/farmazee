from django.contrib import admin
from .models import (
    SoilType, SoilTip, SoilTest, SoilTestResult, SoilHealthRecord,
    FertilizerRecommendation, SoilImprovement, SoilConservation,
    SoilMonitoringSchedule, SoilHealthAlert
)

@admin.register(SoilType)
class SoilTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active']

@admin.register(SoilTip)
class SoilTipAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_featured', 'is_active']
    list_filter = ['category', 'is_featured', 'is_active']
    search_fields = ['title', 'content']
    list_editable = ['is_featured', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Tip Information', {
            'fields': ('title', 'category', 'content', 'image')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SoilTest)
class SoilTestAdmin(admin.ModelAdmin):
    list_display = ['user', 'test_type', 'test_date', 'location', 'is_completed']
    list_filter = ['test_type', 'is_completed', 'test_date']
    search_fields = ['user__username', 'location', 'notes']
    list_editable = ['is_completed']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Test Information', {
            'fields': ('user', 'test_type', 'test_date', 'location')
        }),
        ('Test Details', {
            'fields': ('soil_depth', 'sample_weight', 'notes')
        }),
        ('Status', {
            'fields': ('is_completed',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SoilTestResult)
class SoilTestResultAdmin(admin.ModelAdmin):
    list_display = ['soil_test', 'parameter', 'value', 'unit', 'status']
    list_filter = ['parameter', 'status']
    search_fields = ['soil_test__user__username', 'parameter']
    list_editable = ['status']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Result Information', {
            'fields': ('soil_test', 'parameter', 'value', 'unit')
        }),
        ('Analysis', {
            'fields': ('status', 'recommendation')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SoilHealthRecord)
class SoilHealthRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'record_date', 'soil_type', 'ph_level', 'organic_matter', 'is_healthy']
    list_filter = ['soil_type', 'is_healthy', 'record_date']
    search_fields = ['user__username', 'location', 'notes']
    list_editable = ['is_healthy']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Record Information', {
            'fields': ('user', 'record_date', 'location', 'soil_type')
        }),
        ('Soil Properties', {
            'fields': ('ph_level', 'organic_matter', 'nitrogen', 'phosphorus', 'potassium')
        }),
        ('Additional Properties', {
            'fields': ('calcium', 'magnesium', 'sulfur', 'micronutrients')
        }),
        ('Health Assessment', {
            'fields': ('is_healthy', 'health_score', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(FertilizerRecommendation)
class FertilizerRecommendationAdmin(admin.ModelAdmin):
    list_display = ['soil_test_result', 'fertilizer_name', 'application_rate', 'application_method', 'is_active']
    list_filter = ['application_method', 'is_active']
    search_fields = ['soil_test_result__parameter', 'fertilizer_name', 'recommendation']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Recommendation Information', {
            'fields': ('soil_test_result', 'fertilizer_name', 'application_rate', 'application_method')
        }),
        ('Details', {
            'fields': ('recommendation', 'precautions')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SoilImprovement)
class SoilImprovementAdmin(admin.ModelAdmin):
    list_display = ['user', 'improvement_type', 'start_date', 'end_date', 'status', 'effectiveness']
    list_filter = ['improvement_type', 'status', 'effectiveness', 'start_date']
    search_fields = ['user__username', 'description', 'location']
    list_editable = ['status', 'effectiveness']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Improvement Information', {
            'fields': ('user', 'improvement_type', 'description', 'location')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date')
        }),
        ('Progress', {
            'fields': ('status', 'progress_percentage', 'effectiveness')
        }),
        ('Results', {
            'fields': ('results', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SoilConservation)
class SoilConservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'conservation_type', 'implementation_date', 'status', 'effectiveness']
    list_filter = ['conservation_type', 'status', 'effectiveness', 'implementation_date']
    search_fields = ['user__username', 'description', 'location']
    list_editable = ['status', 'effectiveness']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Conservation Information', {
            'fields': ('user', 'conservation_type', 'description', 'location')
        }),
        ('Implementation', {
            'fields': ('implementation_date', 'cost', 'funding_source')
        }),
        ('Status', {
            'fields': ('status', 'effectiveness')
        }),
        ('Monitoring', {
            'fields': ('monitoring_frequency', 'last_monitoring_date', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SoilMonitoringSchedule)
class SoilMonitoringScheduleAdmin(admin.ModelAdmin):
    list_display = ['user', 'monitoring_type', 'frequency', 'next_monitoring_date', 'is_active']
    list_filter = ['monitoring_type', 'frequency', 'is_active']
    search_fields = ['user__username', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Schedule Information', {
            'fields': ('user', 'monitoring_type', 'description')
        }),
        ('Timing', {
            'fields': ('frequency', 'next_monitoring_date')
        }),
        ('Settings', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SoilHealthAlert)
class SoilHealthAlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'alert_type', 'severity', 'is_active', 'created_at']
    list_filter = ['alert_type', 'severity', 'is_active', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    list_editable = ['is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('user', 'alert_type', 'title', 'message')
        }),
        ('Severity', {
            'fields': ('severity',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
