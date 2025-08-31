"""
Advanced Admin Interface for AI/ML Models in Farmazee Enterprise Platform.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    AIModel, Prediction, ComputerVisionAnalysis, 
    Recommendation, TrainingJob, DataSource
)


@admin.register(AIModel)
class AIModelAdmin(admin.ModelAdmin):
    """Admin interface for AI/ML models."""
    
    list_display = [
        'name', 'model_type', 'version', 'status', 'accuracy', 
        'training_data_size', 'last_trained', 'created_by'
    ]
    
    list_filter = [
        'model_type', 'status', 'created_at', 'last_trained',
        ('accuracy', admin.EmptyFieldListFilter),
    ]
    
    search_fields = ['name', 'description', 'version']
    
    list_editable = ['status', 'version']
    
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'training_duration',
        'accuracy', 'precision', 'recall', 'f1_score'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'model_type', 'version', 'description', 'status')
        }),
        ('Model Files', {
            'fields': ('model_file', 'weights_file', 'config_file'),
            'classes': ('collapse',)
        }),
        ('Performance Metrics', {
            'fields': ('accuracy', 'precision', 'recall', 'f1_score'),
            'classes': ('collapse',)
        }),
        ('Training Information', {
            'fields': ('training_data_size', 'training_duration', 'last_trained'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_models', 'deactivate_models', 'retrain_models']
    
    def activate_models(self, request, queryset):
        """Activate selected models."""
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} models activated successfully.')
    activate_models.short_description = "Activate selected models"
    
    def deactivate_models(self, request, queryset):
        """Deactivate selected models."""
        updated = queryset.update(status='inactive')
        self.message_user(request, f'{updated} models deactivated successfully.')
    deactivate_models.short_description = "Deactivate selected models"
    
    def retrain_models(self, request, queryset):
        """Schedule retraining for selected models."""
        # This would typically create training jobs
        self.message_user(request, f'Retraining scheduled for {queryset.count()} models.')
    retrain_models.short_description = "Schedule retraining for selected models"


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    """Admin interface for AI predictions."""
    
    list_display = [
        'prediction_type', 'user', 'model', 'confidence_score', 
        'confidence_level', 'created_at'
    ]
    
    list_filter = [
        'prediction_type', 'confidence_level', 'created_at',
        'model__model_type'
    ]
    
    search_fields = ['user__username', 'user__email', 'model__name']
    
    readonly_fields = ['id', 'created_at', 'expires_at']
    
    fieldsets = (
        ('Prediction Details', {
            'fields': ('prediction_type', 'model', 'user')
        }),
        ('Results', {
            'fields': ('input_data', 'prediction_result', 'confidence_score', 'confidence_level')
        }),
        ('Metadata', {
            'fields': ('created_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('user', 'model')


@admin.register(ComputerVisionAnalysis)
class ComputerVisionAnalysisAdmin(admin.ModelAdmin):
    """Admin interface for computer vision analysis."""
    
    list_display = [
        'analysis_type', 'user', 'processing_time', 'model_version',
        'created_at', 'image_preview'
    ]
    
    list_filter = [
        'analysis_type', 'created_at', 'model_version'
    ]
    
    search_fields = ['user__username', 'location', 'notes']
    
    readonly_fields = [
        'id', 'created_at', 'processing_time', 'thumbnail'
    ]
    
    fieldsets = (
        ('Analysis Details', {
            'fields': ('analysis_type', 'user', 'location', 'notes')
        }),
        ('Image Data', {
            'fields': ('image', 'thumbnail'),
            'classes': ('collapse',)
        }),
        ('Results', {
            'fields': ('analysis_result', 'detected_objects', 'confidence_scores'),
            'classes': ('collapse',)
        }),
        ('Processing', {
            'fields': ('processing_time', 'model_version'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        """Display image thumbnail in list view."""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.thumbnail.url
            )
        return "No image"
    image_preview.short_description = "Image Preview"


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    """Admin interface for AI recommendations."""
    
    list_display = [
        'title', 'user', 'recommendation_type', 'priority', 
        'confidence_score', 'is_read', 'is_applied', 'created_at'
    ]
    
    list_filter = [
        'recommendation_type', 'priority', 'is_read', 'is_applied',
        'created_at', 'expires_at'
    ]
    
    search_fields = ['title', 'description', 'user__username']
    
    list_editable = ['priority', 'is_read']
    
    readonly_fields = [
        'id', 'created_at', 'expires_at', 'applied_at'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'user', 'recommendation_type', 'priority')
        }),
        ('Content', {
            'fields': ('description', 'action_items', 'expected_benefits')
        }),
        ('AI Analysis', {
            'fields': ('confidence_score', 'reasoning', 'supporting_data'),
            'classes': ('collapse',)
        }),
        ('User Interaction', {
            'fields': ('is_read', 'is_applied', 'applied_at', 'feedback_rating', 'feedback_comment')
        }),
        ('Metadata', {
            'fields': ('location', 'created_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['mark_as_read', 'mark_as_applied', 'send_notifications']
    
    def mark_as_read(self, request, queryset):
        """Mark selected recommendations as read."""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} recommendations marked as read.')
    mark_as_read.short_description = "Mark as read"
    
    def mark_as_applied(self, request, queryset):
        """Mark selected recommendations as applied."""
        updated = queryset.update(is_applied=True)
        self.message_user(request, f'{updated} recommendations marked as applied.')
    mark_as_applied.short_description = "Mark as applied"
    
    def send_notifications(self, request, queryset):
        """Send notifications for selected recommendations."""
        self.message_user(request, f'Notifications sent for {queryset.count()} recommendations.')
    send_notifications.short_description = "Send notifications"


@admin.register(TrainingJob)
class TrainingJobAdmin(admin.ModelAdmin):
    """Admin interface for AI model training jobs."""
    
    list_display = [
        'model', 'user', 'status', 'progress_percentage', 
        'current_epoch', 'total_epochs', 'started_at', 'duration'
    ]
    
    list_filter = [
        'status', 'started_at', 'completed_at', 'model__model_type'
    ]
    
    search_fields = ['model__name', 'user__username']
    
    list_editable = ['status']
    
    readonly_fields = [
        'id', 'created_at', 'updated_at', 'duration'
    ]
    
    fieldsets = (
        ('Job Information', {
            'fields': ('model', 'user', 'status')
        }),
        ('Configuration', {
            'fields': ('training_config', 'dataset_info'),
            'classes': ('collapse',)
        }),
        ('Progress', {
            'fields': ('progress_percentage', 'current_epoch', 'total_epochs')
        }),
        ('Performance', {
            'fields': ('training_loss', 'validation_loss', 'training_accuracy', 'validation_accuracy'),
            'classes': ('collapse',)
        }),
        ('Timing', {
            'fields': ('started_at', 'completed_at', 'duration'),
            'classes': ('collapse',)
        }),
        ('Logs & Artifacts', {
            'fields': ('training_logs', 'error_message', 'artifacts_path'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['cancel_jobs', 'restart_jobs', 'cleanup_completed']
    
    def cancel_jobs(self, request, queryset):
        """Cancel selected training jobs."""
        updated = queryset.filter(status='running').update(status='cancelled')
        self.message_user(request, f'{updated} training jobs cancelled.')
    cancel_jobs.short_description = "Cancel running jobs"
    
    def restart_jobs(self, request, queryset):
        """Restart failed training jobs."""
        updated = queryset.filter(status='failed').update(status='pending')
        self.message_user(request, f'{updated} failed jobs restarted.')
    restart_jobs.short_description = "Restart failed jobs"
    
    def cleanup_completed(self, request, queryset):
        """Clean up completed training jobs."""
        updated = queryset.filter(status='completed').delete()
        self.message_user(request, f'{updated[0]} completed jobs cleaned up.')
    cleanup_completed.short_description = "Clean up completed jobs"


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    """Admin interface for data sources."""
    
    list_display = [
        'name', 'source_type', 'data_format', 'update_frequency',
        'data_quality_score', 'is_active', 'created_at'
    ]
    
    list_filter = [
        'source_type', 'is_active', 'created_at', 'updated_at'
    ]
    
    search_fields = ['name', 'description']
    
    list_editable = ['is_active', 'data_quality_score']
    
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'source_type', 'description')
        }),
        ('Data Characteristics', {
            'fields': ('data_format', 'update_frequency', 'data_quality_score')
        }),
        ('Access Information', {
            'fields': ('access_url', 'api_key_required', 'rate_limit'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    actions = ['activate_sources', 'deactivate_sources', 'update_quality_scores']
    
    def activate_sources(self, request, queryset):
        """Activate selected data sources."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} data sources activated.')
    activate_sources.short_description = "Activate selected sources"
    
    def deactivate_sources(self, request, queryset):
        """Deactivate selected data sources."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} data sources deactivated.')
    deactivate_sources.short_description = "Deactivate selected sources"
    
    def update_quality_scores(self, request, queryset):
        """Update data quality scores."""
        # This would typically trigger a quality assessment task
        self.message_user(request, f'Quality assessment scheduled for {queryset.count()} sources.')
    update_quality_scores.short_description = "Update quality scores"


# Customize admin site
admin.site.site_header = "Farmazee Enterprise Admin"
admin.site.site_title = "Farmazee Admin Portal"
admin.site.index_title = "Welcome to Farmazee Enterprise Platform"

