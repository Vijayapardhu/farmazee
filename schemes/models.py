from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords


class GovernmentScheme(models.Model):
    """Government scheme model"""
    SCHEME_CATEGORIES = [
        ('subsidy', 'Subsidy'),
        ('loan', 'Loan'),
        ('insurance', 'Insurance'),
        ('training', 'Training'),
        ('infrastructure', 'Infrastructure'),
        ('technology', 'Technology'),
        ('marketing', 'Marketing'),
        ('organic', 'Organic Farming'),
        ('disaster_relief', 'Disaster Relief'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=SCHEME_CATEGORIES)
    eligibility_criteria = models.TextField()
    benefits = models.TextField()
    application_process = models.TextField()
    required_documents = models.TextField()
    contact_information = models.TextField()
    website_url = models.URLField(blank=True, null=True)
    helpline_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Scheme details
    scheme_amount = models.CharField(max_length=100, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    states = models.CharField(max_length=500, help_text='Comma-separated list of applicable states')
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Statistics
    views = models.IntegerField(default=0)
    applications_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
    class Meta:
        verbose_name = _('Government Scheme')
        verbose_name_plural = _('Government Schemes')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title


class SchemeApplication(models.Model):
    """Scheme application model"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('closed', 'Closed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheme_applications')
    scheme = models.ForeignKey(GovernmentScheme, on_delete=models.CASCADE, related_name='applications')
    application_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    # Farm Information
    land_area = models.DecimalField(max_digits=8, decimal_places=2, help_text='Land area in acres')
    land_type = models.CharField(max_length=100)
    primary_crop = models.CharField(max_length=100)
    
    # Application Details
    purpose = models.TextField()
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    supporting_documents = models.TextField(blank=True, null=True)
    
    # Timestamps
    applied_date = models.DateTimeField(auto_now_add=True)
    submitted_date = models.DateTimeField(blank=True, null=True)
    reviewed_date = models.DateTimeField(blank=True, null=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    disbursed_date = models.DateTimeField(blank=True, null=True)
    
    # Admin fields
    admin_notes = models.TextField(blank=True, null=True)
    rejection_reason = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-applied_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.scheme.title} - {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.application_number and self.status == 'submitted':
            # Generate application number
            import random
            import string
            self.application_number = f"SCHEME{random.randint(1000, 9999)}{string.ascii_uppercase[random.randint(0, 25)]}"
        super().save(*args, **kwargs)


class SchemeDocument(models.Model):
    """Documents uploaded for scheme applications"""
    application = models.ForeignKey(SchemeApplication, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=100)
    document_file = models.FileField(upload_to='scheme_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verification_notes = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.application.user.username} - {self.document_type}"


class SchemeUpdate(models.Model):
    """Scheme updates and notifications"""
    scheme = models.ForeignKey(GovernmentScheme, on_delete=models.CASCADE, related_name='updates')
    title = models.CharField(max_length=200)
    content = models.TextField()
    update_type = models.CharField(max_length=50, choices=[
        ('deadline', 'Deadline Update'),
        ('criteria', 'Criteria Update'),
        ('amount', 'Amount Update'),
        ('process', 'Process Update'),
        ('general', 'General Update'),
    ])
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.scheme.title} - {self.title}"


class SchemeFAQ(models.Model):
    """Frequently asked questions about schemes"""
    scheme = models.ForeignKey(GovernmentScheme, on_delete=models.CASCADE, related_name='faqs')
    question = models.TextField()
    answer = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'question']
        verbose_name = 'Scheme FAQ'
        verbose_name_plural = 'Scheme FAQs'
    
    def __str__(self):
        return f"{self.scheme.title} - {self.question[:50]}..."


class SchemeSuccessStory(models.Model):
    """Success stories of scheme beneficiaries"""
    scheme = models.ForeignKey(GovernmentScheme, on_delete=models.CASCADE, related_name='success_stories')
    beneficiary_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    story_title = models.CharField(max_length=200)
    story_content = models.TextField()
    benefits_received = models.TextField()
    impact_description = models.TextField()
    before_image = models.ImageField(upload_to='success_stories/', blank=True, null=True)
    after_image = models.ImageField(upload_to='success_stories/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Scheme Success Stories'
    
    def __str__(self):
        return f"{self.beneficiary_name} - {self.story_title}"


class SchemeContact(models.Model):
    """Contact information for scheme queries"""
    scheme = models.ForeignKey(GovernmentScheme, on_delete=models.CASCADE, related_name='contacts')
    contact_person = models.CharField(max_length=200)
    designation = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    office_address = models.TextField()
    office_hours = models.CharField(max_length=100, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'contact_person']
    
    def __str__(self):
        return f"{self.contact_person} - {self.scheme.title}"


class SchemeTimeline(models.Model):
    """Important dates and timeline for schemes"""
    scheme = models.ForeignKey(GovernmentScheme, on_delete=models.CASCADE, related_name='timeline_events')
    event_title = models.CharField(max_length=200)
    event_date = models.DateField()
    event_type = models.CharField(max_length=50, choices=[
        ('announcement', 'Announcement'),
        ('application_start', 'Application Start'),
        ('application_end', 'Application End'),
        ('review_start', 'Review Start'),
        ('review_end', 'Review End'),
        ('approval', 'Approval'),
        ('disbursement', 'Disbursement'),
        ('other', 'Other'),
    ])
    description = models.TextField()
    is_important = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['event_date']
    
    def __str__(self):
        return f"{self.scheme.title} - {self.event_title} - {self.event_date}"


class SchemeNotification(models.Model):
    """Notifications for scheme updates"""
    NOTIFICATION_TYPES = [
        ('deadline_reminder', 'Deadline Reminder'),
        ('status_update', 'Status Update'),
        ('document_required', 'Document Required'),
        ('approval', 'Approval'),
        ('rejection', 'Rejection'),
        ('disbursement', 'Disbursement'),
        ('general', 'General'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='scheme_notifications')
    scheme_application = models.ForeignKey(SchemeApplication, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class SchemeFeedback(models.Model):
    """Feedback from scheme applicants"""
    application = models.ForeignKey(SchemeApplication, on_delete=models.CASCADE, related_name='feedback')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    feedback_text = models.TextField()
    category = models.CharField(max_length=50, choices=[
        ('application_process', 'Application Process'),
        ('documentation', 'Documentation'),
        ('communication', 'Communication'),
        ('timeline', 'Timeline'),
        ('support', 'Support'),
        ('overall', 'Overall Experience'),
    ])
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.application.user.username} - {self.get_category_display()} - {self.rating} stars"

