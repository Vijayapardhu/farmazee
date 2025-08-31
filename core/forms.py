from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    UserProfile, Contact, Notification,
    LoanApplication, InsuranceApplication,
    StorageFacility, ProcessingService, TransportationService,
    Article, Video, FAQ
)


class CustomUserCreationForm(UserCreationForm):
    """Custom user creation form with additional fields"""
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email


class UserProfileForm(forms.ModelForm):
    """User profile form"""
    class Meta:
        model = UserProfile
        fields = [
            'phone_number', 'address', 'village', 'district', 'state', 
            'country', 'pincode', 'land_area', 'primary_crop', 'farm_type',
            'experience_years', 'preferred_language', 'sms_notifications',
            'email_notifications', 'profile_picture'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your address'}),
            'village': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter village name'}),
            'district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter district name'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter state name'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pincode'}),
            'land_area': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Land area in acres'}),
            'primary_crop': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter primary crop'}),
            'farm_type': forms.Select(attrs={'class': 'form-control'}),
            'experience_years': forms.Select(attrs={'class': 'form-control'}),
            'preferred_language': forms.Select(attrs={'class': 'form-control'}),
            'sms_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email_notifications': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class ContactForm(forms.ModelForm):
    """Contact form"""
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Your message'}),
        }


# Financial Services Forms
class LoanApplicationForm(forms.ModelForm):
    """Loan application form"""
    class Meta:
        model = LoanApplication
        fields = [
            'loan_product', 'amount_requested', 'purpose'
        ]
        widgets = {
            'loan_product': forms.Select(attrs={'class': 'form-control'}),
            'amount_requested': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount in INR'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the purpose of the loan'}),
        }


class InsuranceApplicationForm(forms.ModelForm):
    """Insurance application form"""
    class Meta:
        model = InsuranceApplication
        fields = [
            'insurance_product'
        ]
        widgets = {
            'insurance_product': forms.Select(attrs={'class': 'form-control'}),
        }


# Post-Harvest Support Forms
class StorageFacilityForm(forms.ModelForm):
    """Storage facility form"""
    class Meta:
        model = StorageFacility
        fields = [
            'name', 'facility_type', 'location', 'capacity', 'contact_person',
            'phone_number', 'email', 'description', 'services_offered', 'pricing'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facility name'}),
            'facility_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Storage capacity'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Facility description'}),
            'services_offered': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Services offered'}),
            'pricing': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Pricing information'}),
        }


class ProcessingServiceForm(forms.ModelForm):
    """Processing service form"""
    class Meta:
        model = ProcessingService
        fields = [
            'name', 'service_type', 'description', 'suitable_crops',
            'processing_capacity', 'contact_person', 'phone_number',
            'email', 'location', 'pricing'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service name'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Service description'}),
            'suitable_crops': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Suitable crops'}),
            'processing_capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Processing capacity'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'pricing': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Pricing information'}),
        }


class TransportationServiceForm(forms.ModelForm):
    """Transportation service form"""
    class Meta:
        model = TransportationService
        fields = [
            'service_name', 'vehicle_type', 'capacity', 'service_areas',
            'contact_person', 'phone_number', 'email', 'pricing'
        ]
        widgets = {
            'service_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service name'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'capacity': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Vehicle capacity'}),
            'service_areas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Service areas'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact person name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'pricing': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Pricing information'}),
        }


# Knowledge & Support Forms
class ArticleForm(forms.ModelForm):
    """Article form"""
    class Meta:
        model = Article
        fields = [
            'title', 'category', 'content', 'summary', 'author', 'image',
            'is_featured', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Article title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Article content'}),
            'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Article summary'}),
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Author name'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class VideoForm(forms.ModelForm):
    """Video form"""
    class Meta:
        model = Video
        fields = [
            'title', 'category', 'description', 'video_url', 'thumbnail',
            'duration', 'is_featured', 'is_published'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Video title'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Video description'}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Video URL (YouTube, Vimeo, etc.)'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Duration (e.g., 5:30)'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class FAQForm(forms.ModelForm):
    """FAQ form"""
    class Meta:
        model = FAQ
        fields = [
            'question', 'answer', 'category', 'is_active', 'order'
        ]
        widgets = {
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Question'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Answer'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Display order'}),
        }
