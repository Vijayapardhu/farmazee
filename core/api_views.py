from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.utils import timezone
from .models import UserProfile, Notification, FAQ, Contact
from .serializers import (
    UserSerializer, UserProfileSerializer, NotificationSerializer,
    FAQSerializer, ContactSerializer
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """User viewset for API"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserProfileViewSet(viewsets.ModelViewSet):
    """UserProfile viewset for API"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NotificationViewSet(viewsets.ModelViewSet):
    """Notification viewset for API"""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'success'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'status': 'success'})


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """FAQ viewset for API"""
    queryset = FAQ.objects.filter(is_active=True)
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = FAQ.objects.filter(is_active=True)
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset


class ContactViewSet(viewsets.ModelViewSet):
    """Contact viewset for API"""
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        serializer.save()


class SearchAPIView(APIView):
    """Global search API"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        results = {}
        
        # Search in crops
        try:
            from crops.models import Crop
            crops = Crop.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )[:10]
            results['crops'] = [{'id': crop.id, 'name': crop.name} for crop in crops]
        except ImportError:
            results['crops'] = []
        
        # Search in products
        try:
            from marketplace.models import Product
            products = Product.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )[:10]
            results['products'] = [{'id': product.id, 'name': product.name} for product in products]
        except ImportError:
            results['products'] = []
        
        # Search in schemes
        try:
            from schemes.models import GovernmentScheme
            schemes = GovernmentScheme.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__icontains=query)
            )[:10]
            results['schemes'] = [{'id': scheme.id, 'title': scheme.title} for scheme in schemes]
        except ImportError:
            results['schemes'] = []
        
        # Search in soil tips
        try:
            from soil_health.models import SoilTip
            soil_tips = SoilTip.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )[:10]
            results['soil_tips'] = [{'id': tip.id, 'title': tip.title} for tip in soil_tips]
        except ImportError:
            results['soil_tips'] = []
        
        return Response(results)


class StatsAPIView(APIView):
    """Statistics API"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        stats = {
            'total_farmers': UserProfile.objects.count(),
            'total_crops': 0,
            'total_products': 0,
            'total_schemes': 0,
            'total_soil_tips': 0,
            'active_weather_locations': 0,
        }
        
        try:
            from crops.models import Crop
            stats['total_crops'] = Crop.objects.count()
        except ImportError:
            pass
            
        try:
            from marketplace.models import Product
            stats['total_products'] = Product.objects.count()
        except ImportError:
            pass
            
        try:
            from schemes.models import GovernmentScheme
            stats['total_schemes'] = GovernmentScheme.objects.count()
        except ImportError:
            pass
            
        try:
            from soil_health.models import SoilTip
            stats['total_soil_tips'] = SoilTip.objects.count()
        except ImportError:
            pass
            
        try:
            from weather.models import WeatherData
            stats['active_weather_locations'] = WeatherData.objects.filter(is_current=True).count()
        except ImportError:
            pass
        
        return Response(stats)


class WeatherAPIView(APIView):
    """Weather API endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            from weather.advanced_weather_service import advanced_weather_service
            
            # Get current weather data
            current_weather = advanced_weather_service.get_current_weather('Hyderabad')
            
            return Response({
                'status': 'success',
                'data': {
                    'current_weather': current_weather,
                    'timestamp': timezone.now().isoformat()
                }
            })
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MarketplacePricesAPIView(APIView):
    """Marketplace prices API endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            from marketplace.price_services import get_market_prices
            
            # Get market prices
            prices = get_market_prices()
            
            return Response({
                'status': 'success',
                'data': {
                    'prices': prices,
                    'timestamp': timezone.now().isoformat()
                }
            })
        except Exception as e:
            # Return mock data if service fails
            mock_prices = [
                {'name': 'Rice', 'price': '₹2,500', 'unit': 'per quintal', 'change': '+2.5%'},
                {'name': 'Wheat', 'price': '₹2,100', 'unit': 'per quintal', 'change': '+1.8%'},
                {'name': 'Tomato', 'price': '₹45', 'unit': 'per kg', 'change': '-3.2%'},
                {'name': 'Onion', 'price': '₹35', 'unit': 'per kg', 'change': '+5.1%'},
                {'name': 'Potato', 'price': '₹25', 'unit': 'per kg', 'change': '+1.2%'},
            ]
            
            return Response({
                'status': 'success',
                'data': {
                    'prices': mock_prices,
                    'timestamp': timezone.now().isoformat(),
                    'note': 'Mock data - service unavailable'
                }
            })
