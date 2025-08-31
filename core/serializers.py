from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Notification, FAQ, Contact, Language


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class LanguageSerializer(serializers.ModelSerializer):
    """Language serializer"""
    class Meta:
        model = Language
        fields = ['id', 'code', 'name', 'native_name']


class UserProfileSerializer(serializers.ModelSerializer):
    """UserProfile serializer"""
    user = UserSerializer(read_only=True)
    preferred_language = LanguageSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'phone_number', 'address', 'village', 'district', 
            'state', 'country', 'pincode', 'land_area', 'primary_crop',
            'preferred_language', 'sms_notifications', 'email_notifications',
            'profile_picture', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class NotificationSerializer(serializers.ModelSerializer):
    """Notification serializer"""
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'message', 'is_read',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class FAQSerializer(serializers.ModelSerializer):
    """FAQ serializer"""
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'created_at']
        read_only_fields = ['id', 'created_at']


class ContactSerializer(serializers.ModelSerializer):
    """Contact serializer"""
    class Meta:
        model = Contact
        fields = ['id', 'name', 'email', 'subject', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """User registration serializer"""
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
    
    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=password,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user
