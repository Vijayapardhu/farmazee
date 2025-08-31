from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatSession(models.Model):
    """Chat session for a farmer"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"Chat Session {self.session_id} - {self.user.username}"


class ChatMessage(models.Model):
    """Individual chat message"""
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('assistant', 'AI Assistant'),
        ('system', 'System Message'),
    ]
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    tokens_used = models.IntegerField(default=0)
    response_time = models.FloatField(default=0.0)  # in seconds
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.message_type} - {self.timestamp.strftime('%H:%M')}"


class FarmerQuery(models.Model):
    """Stored farmer queries for analytics and improvement"""
    QUERY_CATEGORIES = [
        ('crop_management', 'Crop Management'),
        ('pest_control', 'Pest Control'),
        ('soil_health', 'Soil Health'),
        ('weather', 'Weather'),
        ('market_info', 'Market Information'),
        ('government_schemes', 'Government Schemes'),
        ('general', 'General Farming'),
        ('technical', 'Technical Support'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farmer_queries')
    query_text = models.TextField()
    category = models.CharField(max_length=50, choices=QUERY_CATEGORIES)
    ai_response = models.TextField()
    satisfaction_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_helpful = models.BooleanField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.category} - {self.query_text[:50]}..."


class AIKnowledgeBase(models.Model):
    """Knowledge base for AI responses"""
    KNOWLEDGE_TYPES = [
        ('crop_info', 'Crop Information'),
        ('pest_disease', 'Pest & Disease'),
        ('soil_management', 'Soil Management'),
        ('weather_patterns', 'Weather Patterns'),
        ('best_practices', 'Best Practices'),
        ('market_trends', 'Market Trends'),
        ('government_policies', 'Government Policies'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    knowledge_type = models.CharField(max_length=50, choices=KNOWLEDGE_TYPES)
    keywords = models.TextField(help_text="Comma-separated keywords for search")
    source = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.title} - {self.knowledge_type}"
