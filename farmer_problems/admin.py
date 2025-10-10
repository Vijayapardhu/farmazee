"""
Admin interface for Farmer Problems app
"""

from django.contrib import admin
from .models import (
    ProblemCategory, FarmerProblem, ProblemImage,
    Solution, SolutionImage, Comment, Vote,
    ExpertProfile, Tag
)


@admin.register(ProblemCategory)
class ProblemCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


class ProblemImageInline(admin.TabularInline):
    model = ProblemImage
    extra = 1
    fields = ['image_url', 'caption', 'order']


@admin.register(FarmerProblem)
class FarmerProblemAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views_count', 'created_at', 'is_pinned']
    list_filter = ['status', 'category', 'is_pinned', 'is_featured', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['views_count', 'created_at', 'updated_at']
    inlines = [ProblemImageInline]
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'author', 'category')
        }),
        ('Location & Crop', {
            'fields': ('location', 'crop_type')
        }),
        ('Status', {
            'fields': ('status', 'is_pinned', 'is_featured')
        }),
        ('Metadata', {
            'fields': ('views_count', 'created_at', 'updated_at', 'solved_at'),
            'classes': ('collapse',)
        }),
    )


class SolutionImageInline(admin.TabularInline):
    model = SolutionImage
    extra = 1
    fields = ['image_url', 'caption', 'order']


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ['get_problem_title', 'author', 'is_expert', 'is_accepted', 'created_at']
    list_filter = ['is_expert', 'is_accepted', 'created_at']
    search_fields = ['content', 'author__username', 'problem__title']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [SolutionImageInline]
    
    def get_problem_title(self, obj):
        return obj.problem.title[:50]
    get_problem_title.short_description = 'Problem'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'comment_type', 'get_content_preview', 'created_at']
    list_filter = ['comment_type', 'created_at']
    search_fields = ['content', 'author__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_content_preview(self, obj):
        return obj.content[:50]
    get_content_preview.short_description = 'Content'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'content_type', 'vote_type', 'created_at']
    list_filter = ['content_type', 'vote_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']


@admin.register(ExpertProfile)
class ExpertProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'expert_type', 'is_verified', 'reputation_score', 'solutions_count']
    list_filter = ['expert_type', 'is_verified', 'verified_at']
    search_fields = ['user__username', 'qualification', 'institution']
    readonly_fields = ['solutions_count', 'accepted_solutions_count', 'reputation_score', 'created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'expert_type', 'qualification', 'institution')
        }),
        ('Experience', {
            'fields': ('years_of_experience', 'specialization', 'bio')
        }),
        ('Verification', {
            'fields': ('is_verified', 'verification_document_url', 'verified_at', 'verified_by')
        }),
        ('Statistics', {
            'fields': ('solutions_count', 'accepted_solutions_count', 'reputation_score'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'problem_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']
    
    def problem_count(self, obj):
        return obj.problems.count()
    problem_count.short_description = 'Problems'
