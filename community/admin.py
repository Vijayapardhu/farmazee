from django.contrib import admin
from .models import (
    ForumCategory, ForumTopic, ForumReply, Expert, Question, Answer,
    CommunityEvent, EventRegistration, Consultation, KnowledgeArticle,
    Poll, PollOption, PollVote, Notification
)

@admin.register(ForumCategory)
class ForumCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_active', 'order']

@admin.register(ForumTopic)
class ForumTopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_pinned', 'is_locked', 'is_active', 'views', 'reply_count']
    list_filter = ['category', 'is_pinned', 'is_locked', 'is_active']
    search_fields = ['title', 'content', 'author__username']
    list_editable = ['is_pinned', 'is_locked', 'is_active']
    readonly_fields = ['views', 'reply_count', 'last_reply_at', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Topic Information', {
            'fields': ('author', 'category', 'title', 'content')
        }),
        ('Settings', {
            'fields': ('is_pinned', 'is_locked', 'is_active')
        }),
        ('Statistics', {
            'fields': ('views', 'reply_count', 'last_reply_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ['topic', 'author', 'is_solution', 'likes']
    list_filter = ['is_solution']
    search_fields = ['topic__title', 'author__username', 'content']
    list_editable = ['is_solution']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'experience_years', 'consultation_fee', 'is_verified', 'is_active', 'rating', 'consultation_count']
    list_filter = ['specialization', 'is_verified', 'is_active', 'experience_years']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'specialization']
    list_editable = ['is_verified', 'is_active']
    readonly_fields = ['rating', 'consultation_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Expert Information', {
            'fields': ('user', 'specialization', 'qualifications', 'experience_years', 'bio')
        }),
        ('Consultation Details', {
            'fields': ('consultation_fee',)
        }),
        ('Status', {
            'fields': ('is_verified', 'is_active')
        }),
        ('Statistics', {
            'fields': ('rating', 'consultation_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'views', 'answer_count']
    list_filter = ['category', 'status', 'is_featured']
    search_fields = ['title', 'content', 'author__username']
    list_editable = ['status', 'is_featured']
    readonly_fields = ['views', 'answer_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Question Information', {
            'fields': ('author', 'category', 'title', 'content')
        }),
        ('Status', {
            'fields': ('status', 'is_featured')
        }),
        ('Best Answer', {
            'fields': ('best_answer',)
        }),
        ('Statistics', {
            'fields': ('views', 'answer_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'author', 'is_best_answer', 'likes']
    list_filter = ['is_best_answer']
    search_fields = ['question__title', 'author__username', 'content']
    list_editable = ['is_best_answer']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CommunityEvent)
class CommunityEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'location', 'event_date', 'organizer', 'is_active', 'is_free']
    list_filter = ['event_type', 'is_active', 'is_free', 'event_date']
    search_fields = ['title', 'description', 'location', 'organizer__username']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'event_type', 'description', 'location', 'event_date', 'duration')
        }),
        ('Organizer', {
            'fields': ('organizer',)
        }),
        ('Registration', {
            'fields': ('max_participants', 'registration_deadline', 'is_free', 'fee_amount')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'registration_date', 'is_confirmed', 'payment_status']
    list_filter = ['is_confirmed', 'payment_status', 'registration_date']
    search_fields = ['event__title', 'user__username']
    list_editable = ['is_confirmed', 'payment_status']
    readonly_fields = ['registration_date']

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ['user', 'expert', 'consultation_type', 'subject', 'status', 'scheduled_date', 'fee', 'payment_status']
    list_filter = ['consultation_type', 'status', 'payment_status', 'scheduled_date']
    search_fields = ['user__username', 'expert__user__username', 'subject']
    list_editable = ['status', 'payment_status']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Consultation Information', {
            'fields': ('user', 'expert', 'consultation_type', 'subject', 'description')
        }),
        ('Scheduling', {
            'fields': ('status', 'scheduled_date', 'duration')
        }),
        ('Financial', {
            'fields': ('fee', 'payment_status')
        }),
        ('Feedback', {
            'fields': ('expert_notes', 'user_feedback', 'rating')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(KnowledgeArticle)
class KnowledgeArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_featured', 'is_published', 'views', 'likes']
    list_filter = ['category', 'is_featured', 'is_published']
    search_fields = ['title', 'content', 'author__username']
    list_editable = ['is_featured', 'is_published']
    readonly_fields = ['views', 'likes', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Article Information', {
            'fields': ('author', 'category', 'title', 'content', 'summary')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('SEO & Tags', {
            'fields': ('tags',)
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_published')
        }),
        ('Statistics', {
            'fields': ('views', 'likes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'is_active', 'end_date']
    list_filter = ['is_active', 'end_date']
    search_fields = ['title', 'description', 'created_by__username']
    list_editable = ['is_active']

@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    list_display = ['poll', 'option_text', 'vote_count']
    list_filter = ['poll__is_active']
    search_fields = ['poll__title', 'option_text']
    readonly_fields = ['vote_count']

@admin.register(PollVote)
class PollVoteAdmin(admin.ModelAdmin):
    list_display = ['poll', 'option', 'user', 'voted_at']
    list_filter = ['voted_at']
    search_fields = ['poll__title', 'option__option_text', 'user__username']
    readonly_fields = ['voted_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'is_read']
    list_filter = ['notification_type', 'is_read']
    search_fields = ['user__username', 'title', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('user', 'notification_type', 'title', 'message')
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
