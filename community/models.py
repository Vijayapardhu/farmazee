from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ForumCategory(models.Model):
    """Forum category model"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, null=True)
    color = models.CharField(max_length=7, default='#007bff', help_text='Hex color code')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = _('Forum Category')
        verbose_name_plural = _('Forum Categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class ForumTopic(models.Model):
    """Forum topic model"""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_topics')
    category = models.ForeignKey(ForumCategory, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    reply_count = models.IntegerField(default=0)
    last_reply_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Forum Topic')
        verbose_name_plural = _('Forum Topics')
        ordering = ['-is_pinned', '-last_reply_at', '-created_at']
    
    def __str__(self):
        return self.title


class ForumReply(models.Model):
    """Forum reply model"""
    topic = models.ForeignKey(ForumTopic, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='forum_replies')
    content = models.TextField()
    is_solution = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Forum Reply')
        verbose_name_plural = _('Forum Replies')
        ordering = ['created_at']
    
    def __str__(self):
        return f"Reply to {self.topic.title} by {self.author.username}"


class Expert(models.Model):
    """Expert model for community consultations"""
    EXPERTISE_AREAS = [
        ('crop_production', 'Crop Production'),
        ('soil_health', 'Soil Health'),
        ('pest_management', 'Pest Management'),
        ('irrigation', 'Irrigation'),
        ('organic_farming', 'Organic Farming'),
        ('technology', 'Agricultural Technology'),
        ('marketing', 'Agricultural Marketing'),
        ('finance', 'Agricultural Finance'),
        ('weather', 'Weather & Climate'),
        ('livestock', 'Livestock Management'),
        ('horticulture', 'Horticulture'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='expert_profile')
    specialization = models.CharField(max_length=50, choices=EXPERTISE_AREAS)
    qualifications = models.TextField()
    experience_years = models.IntegerField()
    bio = models.TextField()
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    consultation_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Expert')
        verbose_name_plural = _('Experts')
        ordering = ['-rating', '-consultation_count']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_specialization_display()}"


class Question(models.Model):
    """Question model for Q&A"""
    QUESTION_CATEGORIES = [
        ('crop', 'Crop Management'),
        ('soil', 'Soil Health'),
        ('weather', 'Weather'),
        ('pest', 'Pest Management'),
        ('disease', 'Disease Management'),
        ('market', 'Market Information'),
        ('technology', 'Technology'),
        ('general', 'General'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('answered', 'Answered'),
        ('closed', 'Closed'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    category = models.CharField(max_length=20, choices=QUESTION_CATEGORIES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    is_featured = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    answer_count = models.IntegerField(default=0)
    best_answer = models.ForeignKey('Answer', on_delete=models.SET_NULL, blank=True, null=True, related_name='best_for_question')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Answer(models.Model):
    """Answer model for Q&A"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    is_best_answer = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_best_answer', '-likes', 'created_at']
    
    def __str__(self):
        return f"Answer to {self.question.title} by {self.author.username}"


class CommunityEvent(models.Model):
    """Community events model"""
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('training', 'Training'),
        ('meetup', 'Meetup'),
        ('competition', 'Competition'),
        ('exhibition', 'Exhibition'),
        ('webinar', 'Webinar'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    description = models.TextField()
    location = models.CharField(max_length=200)
    event_date = models.DateTimeField(blank=True, null=True)  # Fixed: made nullable
    duration = models.CharField(max_length=100, blank=True, null=True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    max_participants = models.IntegerField(blank=True, null=True)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    is_free = models.BooleanField(default=True)
    fee_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Community Event')
        verbose_name_plural = _('Community Events')
        ordering = ['event_date']
    
    def __str__(self):
        return f"{self.title} - {self.event_date}"


class EventRegistration(models.Model):
    """Event registration model"""
    event = models.ForeignKey(CommunityEvent, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = ['event', 'user']
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class Consultation(models.Model):
    """Expert consultation model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    CONSULTATION_TYPES = [
        ('chat', 'Chat'),
        ('call', 'Phone Call'),
        ('video', 'Video Call'),
        ('visit', 'Field Visit'),
        ('report', 'Written Report'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='consultations')
    expert = models.ForeignKey(Expert, on_delete=models.CASCADE, related_name='consultations')
    consultation_type = models.CharField(max_length=20, choices=CONSULTATION_TYPES)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    scheduled_date = models.DateTimeField(blank=True, null=True)
    duration = models.IntegerField(help_text='Duration in minutes', blank=True, null=True)
    fee = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    payment_status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ], default='pending')
    expert_notes = models.TextField(blank=True, null=True)
    user_feedback = models.TextField(blank=True, null=True)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.expert.user.get_full_name()} - {self.subject}"


class KnowledgeArticle(models.Model):
    """Knowledge sharing articles"""
    CATEGORIES = [
        ('farming_techniques', 'Farming Techniques'),
        ('success_stories', 'Success Stories'),
        ('innovations', 'Innovations'),
        ('best_practices', 'Best Practices'),
        ('case_studies', 'Case Studies'),
        ('research', 'Research'),
        ('tips', 'Tips & Tricks'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='knowledge_articles')
    category = models.CharField(max_length=20, choices=CATEGORIES)
    title = models.CharField(max_length=200)
    content = models.TextField()
    summary = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='knowledge_articles/', blank=True, null=True)
    tags = models.CharField(max_length=500, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class Poll(models.Model):
    """Community polls"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_polls')
    is_active = models.BooleanField(default=True)
    end_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class PollOption(models.Model):
    """Poll options"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='options')
    option_text = models.CharField(max_length=200)
    vote_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['option_text']
    
    def __str__(self):
        return f"{self.poll.title} - {self.option_text}"


class PollVote(models.Model):
    """Poll votes"""
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name='poll_votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poll_votes')
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['poll', 'user']
        verbose_name = 'Poll Vote'
        verbose_name_plural = 'Poll Votes'
    
    def __str__(self):
        return f"{self.user.username} voted for {self.option.option_text} in {self.poll.title}"


class Notification(models.Model):
    """Community notifications"""
    NOTIFICATION_TYPES = [
        ('question_answer', 'Question Answered'),
        ('event_reminder', 'Event Reminder'),
        ('consultation_update', 'Consultation Update'),
        ('poll_result', 'Poll Result'),
        ('expert_response', 'Expert Response'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    related_url = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

