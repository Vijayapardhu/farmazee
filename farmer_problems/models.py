"""
Models for Farmer Problems & Solutions (Reddit-style feature)
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class ProblemCategory(models.Model):
    """Categories for farmer problems"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-question-circle')
    color = models.CharField(max_length=20, default='#28a745')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Problem Categories'
    
    def __str__(self):
        return self.name


class FarmerProblem(models.Model):
    """Main problem post by farmers"""
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('solved', 'Solved'),
        ('closed', 'Closed'),
    ]
    
    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=350, unique=True, blank=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farmer_problems')
    category = models.ForeignKey(ProblemCategory, on_delete=models.SET_NULL, null=True, related_name='problems')
    
    # Location information
    location = models.CharField(max_length=200, blank=True, help_text="Farm location or village")
    crop_type = models.CharField(max_length=100, blank=True)
    
    # Status and metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    views_count = models.IntegerField(default=0)
    is_pinned = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    solved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-is_pinned', '-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('farmer_problems:detail', kwargs={'slug': self.slug})
    
    @property
    def total_votes(self):
        return self.votes.filter(vote_type='up').count() - self.votes.filter(vote_type='down').count()
    
    @property
    def solution_count(self):
        return self.solutions.count()
    
    @solution_count.setter
    def solution_count(self, value):
        # This is a read-only property, so we don't actually set anything
        pass
    
    @property
    def accepted_solution(self):
        return self.solutions.filter(is_accepted=True).first()


class ProblemImage(models.Model):
    """Images attached to problems"""
    problem = models.ForeignKey(FarmerProblem, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500, help_text="Supabase storage URL")
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'uploaded_at']
    
    def __str__(self):
        return f"Image for {self.problem.title}"


class Solution(models.Model):
    """Expert solutions to farmer problems"""
    problem = models.ForeignKey(FarmerProblem, on_delete=models.CASCADE, related_name='solutions')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solutions')
    content = models.TextField()
    
    # Expert verification
    is_expert = models.BooleanField(default=False)
    expert_badge = models.CharField(max_length=100, blank=True, help_text="e.g., Agricultural Expert, PhD")
    
    # Solution status
    is_accepted = models.BooleanField(default=False)
    is_helpful = models.IntegerField(default=0)  # Helpful votes
    
    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_accepted', '-is_helpful', '-created_at']
    
    def __str__(self):
        return f"Solution by {self.author.username} for {self.problem.title[:50]}"
    
    @property
    def total_votes(self):
        return self.votes.filter(vote_type='up').count() - self.votes.filter(vote_type='down').count()


class SolutionImage(models.Model):
    """Images attached to solutions"""
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField(max_length=500, help_text="Supabase storage URL")
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'uploaded_at']
    
    def __str__(self):
        return f"Image for solution by {self.solution.author.username}"


class Comment(models.Model):
    """Comments on problems or solutions"""
    COMMENT_TYPE_CHOICES = [
        ('problem', 'Problem Comment'),
        ('solution', 'Solution Comment'),
    ]
    
    comment_type = models.CharField(max_length=20, choices=COMMENT_TYPE_CHOICES)
    problem = models.ForeignKey(FarmerProblem, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username}"


class Vote(models.Model):
    """Voting system for problems and solutions"""
    VOTE_CHOICES = [
        ('up', 'Upvote'),
        ('down', 'Downvote'),
    ]
    
    CONTENT_TYPE_CHOICES = [
        ('problem', 'Problem'),
        ('solution', 'Solution'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES)
    problem = models.ForeignKey(FarmerProblem, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, null=True, blank=True, related_name='votes')
    vote_type = models.CharField(max_length=10, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [
            ['user', 'problem'],
            ['user', 'solution'],
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.vote_type}"


class ExpertProfile(models.Model):
    """Expert user profiles"""
    EXPERT_TYPE_CHOICES = [
        ('agronomist', 'Agronomist'),
        ('agricultural_scientist', 'Agricultural Scientist'),
        ('extension_officer', 'Extension Officer'),
        ('researcher', 'Researcher'),
        ('veterinarian', 'Veterinarian'),
        ('soil_scientist', 'Soil Scientist'),
        ('experienced_farmer', 'Experienced Farmer'),
        ('other', 'Other Expert'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farming_expert_profile')
    expert_type = models.CharField(max_length=50, choices=EXPERT_TYPE_CHOICES)
    qualification = models.CharField(max_length=200)
    institution = models.CharField(max_length=200, blank=True)
    years_of_experience = models.IntegerField(default=0)
    specialization = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    
    # Verification
    is_verified = models.BooleanField(default=False)
    verification_document_url = models.URLField(max_length=500, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_experts')
    
    # Statistics
    solutions_count = models.IntegerField(default=0)
    accepted_solutions_count = models.IntegerField(default=0)
    reputation_score = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-reputation_score', '-verified_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_expert_type_display()}"
    
    @property
    def acceptance_rate(self):
        if self.solutions_count > 0:
            return (self.accepted_solutions_count / self.solutions_count) * 100
        return 0


class Tag(models.Model):
    """Tags for problems"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    problems = models.ManyToManyField(FarmerProblem, related_name='tags', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
