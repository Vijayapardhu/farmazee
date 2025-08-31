from django.contrib import admin
from .models import (
    GovernmentScheme, SchemeApplication, SchemeDocument, SchemeUpdate,
    SchemeFAQ, SchemeSuccessStory, SchemeContact, SchemeTimeline,
    SchemeNotification, SchemeFeedback
)

@admin.register(GovernmentScheme)
class GovernmentSchemeAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'scheme_amount', 'deadline', 'is_active', 'is_featured', 'views', 'applications_count']
    list_filter = ['category', 'is_active', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'eligibility_criteria']
    list_editable = ['is_active', 'is_featured']
    readonly_fields = ['views', 'applications_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Scheme Details', {
            'fields': ('scheme_amount', 'start_date', 'deadline')
        }),
        ('Eligibility & Requirements', {
            'fields': ('eligibility_criteria', 'required_documents', 'application_process')
        }),
        ('Benefits & Contact', {
            'fields': ('benefits', 'contact_information', 'website_url', 'helpline_number')
        }),
        ('Applicability', {
            'fields': ('states',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('views', 'applications_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SchemeApplication)
class SchemeApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'user', 'scheme', 'status', 'applied_date', 'amount_requested']
    list_filter = ['status', 'applied_date', 'scheme__category']
    search_fields = ['application_number', 'user__username', 'scheme__title', 'full_name']
    list_editable = ['status']
    readonly_fields = ['applied_date', 'submitted_date', 'reviewed_date', 'approved_date', 'disbursed_date']
    
    fieldsets = (
        ('Application Information', {
            'fields': ('user', 'scheme', 'application_number', 'status')
        }),
        ('Personal Information', {
            'fields': ('full_name', 'phone_number', 'email', 'address', 'village', 'district', 'state', 'pincode')
        }),
        ('Farm Information', {
            'fields': ('land_area', 'land_type', 'primary_crop')
        }),
        ('Application Details', {
            'fields': ('purpose', 'amount_requested', 'supporting_documents')
        }),
        ('Timestamps', {
            'fields': ('applied_date', 'submitted_date', 'reviewed_date', 'approved_date', 'disbursed_date')
        }),
        ('Admin Notes', {
            'fields': ('admin_notes', 'rejection_reason')
        }),
    )

@admin.register(SchemeDocument)
class SchemeDocumentAdmin(admin.ModelAdmin):
    list_display = ['application', 'document_type', 'uploaded_at', 'is_verified']
    list_filter = ['document_type', 'is_verified', 'uploaded_at']
    search_fields = ['application__user__username', 'document_type']
    list_editable = ['is_verified']
    readonly_fields = ['uploaded_at']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('application', 'document_type', 'document_file')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_notes')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SchemeUpdate)
class SchemeUpdateAdmin(admin.ModelAdmin):
    list_display = ['scheme', 'title', 'update_type', 'is_important', 'created_at']
    list_filter = ['update_type', 'is_important', 'created_at']
    search_fields = ['scheme__title', 'title', 'content']
    list_editable = ['is_important']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Update Information', {
            'fields': ('scheme', 'title', 'content', 'update_type')
        }),
        ('Settings', {
            'fields': ('is_important',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SchemeFAQ)
class SchemeFAQAdmin(admin.ModelAdmin):
    list_display = ['scheme', 'question', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['scheme__title', 'question', 'answer']
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('FAQ Information', {
            'fields': ('scheme', 'question', 'answer')
        }),
        ('Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SchemeSuccessStory)
class SchemeSuccessStoryAdmin(admin.ModelAdmin):
    list_display = ['scheme', 'beneficiary_name', 'location', 'story_title', 'is_featured', 'is_verified', 'created_at']
    list_filter = ['is_featured', 'is_verified', 'created_at']
    search_fields = ['scheme__title', 'beneficiary_name', 'story_title', 'location']
    list_editable = ['is_featured', 'is_verified']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Story Information', {
            'fields': ('scheme', 'beneficiary_name', 'location', 'story_title', 'story_content')
        }),
        ('Impact', {
            'fields': ('benefits_received', 'impact_description')
        }),
        ('Media', {
            'fields': ('before_image', 'after_image')
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_verified')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SchemeContact)
class SchemeContactAdmin(admin.ModelAdmin):
    list_display = ['scheme', 'contact_person', 'designation', 'phone_number', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['scheme__title', 'contact_person', 'designation', 'phone_number']
    list_editable = ['is_primary']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('scheme', 'contact_person', 'designation', 'phone_number', 'email')
        }),
        ('Office Details', {
            'fields': ('office_address', 'office_hours')
        }),
        ('Settings', {
            'fields': ('is_primary',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SchemeTimeline)
class SchemeTimelineAdmin(admin.ModelAdmin):
    list_display = ['scheme', 'event_title', 'event_date', 'event_type', 'is_important', 'created_at']
    list_filter = ['event_type', 'is_important', 'event_date', 'created_at']
    search_fields = ['scheme__title', 'event_title', 'description']
    list_editable = ['is_important']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Timeline Information', {
            'fields': ('scheme', 'event_title', 'event_date', 'event_type', 'description')
        }),
        ('Settings', {
            'fields': ('is_important',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SchemeNotification)
class SchemeNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'scheme_application', 'notification_type', 'title', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('user', 'scheme_application', 'notification_type', 'title', 'message')
        }),
        ('Link', {
            'fields': ('related_url',)
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(SchemeFeedback)
class SchemeFeedbackAdmin(admin.ModelAdmin):
    list_display = ['application', 'rating', 'category', 'is_anonymous', 'created_at']
    list_filter = ['rating', 'category', 'is_anonymous', 'created_at']
    search_fields = ['application__user__username', 'feedback_text']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Feedback Information', {
            'fields': ('application', 'rating', 'feedback_text', 'category')
        }),
        ('Settings', {
            'fields': ('is_anonymous',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
