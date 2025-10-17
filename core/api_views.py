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
        
        # Crops functionality removed
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
        
        # Crops functionality removed
        stats['total_crops'] = 0
            
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
            from marketplace.services import market_price_service
            
            crop_name = request.GET.get('crop')
            mandi_name = request.GET.get('mandi')
            limit = int(request.GET.get('limit', 10))
            
            # Get live prices using the service
            prices_data = market_price_service.get_live_prices(crop_name, mandi_name, limit)
            
            return Response({
                'status': 'success',
                'data': prices_data,
                'timestamp': timezone.now().isoformat()
            })
        except Exception as e:
            # Return mock data if service fails
            mock_prices = [
                {'name': 'Rice', 'price': '₹2,150', 'unit': 'per quintal', 'change': '+2.5%'},
                {'name': 'Cotton', 'price': '₹6,800', 'unit': 'per quintal', 'change': '+1.8%'},
                {'name': 'Maize', 'price': '₹1,890', 'unit': 'per quintal', 'change': '-1.2%'},
                {'name': 'Chilli', 'price': '₹8,500', 'unit': 'per quintal', 'change': '+5.2%'},
                {'name': 'Wheat', 'price': '₹2,200', 'unit': 'per quintal', 'change': '+0.8%'},
            ]
            
            return Response({
                'status': 'success',
                'data': {
                    'crop': 'All Crops',
                    'prices': mock_prices,
                    'timestamp': timezone.now().isoformat(),
                    'note': 'Mock data - service unavailable'
                }
            })


class SoilTestsAPIView(APIView):
    """Soil tests API endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            from soil_health.models import SoilTest
            
            # Get soil tests for the current user if authenticated
            if request.user.is_authenticated:
                soil_tests = SoilTest.objects.filter(user=request.user).order_by('-test_date')
            else:
                # Return sample data for non-authenticated users
                soil_tests = SoilTest.objects.filter(is_sample=True)[:5]
            
            results = []
            for test in soil_tests:
                results.append({
                    'id': test.id,
                    'testDate': test.test_date.isoformat(),
                    'location': test.location,
                    'soilDepth': test.soil_depth,
                    'phLevel': float(test.ph_level),
                    'organicMatter': float(test.organic_matter),
                    'nitrogen': test.nitrogen,
                    'phosphorus': test.phosphorus,
                    'potassium': test.potassium,
                    'status': test.status,
                    'recommendations': test.recommendations
                })
            
            return Response({
                'status': 'success',
                'results': results,
                'count': len(results),
                'timestamp': timezone.now().isoformat()
            })
        except Exception as e:
            # Return mock data if service fails
            mock_tests = [
                {
                    'id': 1,
                    'testDate': '2025-01-15T10:00:00Z',
                    'location': 'Field A - North Section',
                    'soilDepth': '0-30 cm',
                    'phLevel': 6.8,
                    'organicMatter': 2.1,
                    'nitrogen': 45,
                    'phosphorus': 28,
                    'potassium': 180,
                    'status': 'Completed',
                    'recommendations': 'Good soil health, maintain current practices'
                },
                {
                    'id': 2,
                    'testDate': '2025-01-10T14:30:00Z',
                    'location': 'Field B - South Section',
                    'soilDepth': '0-30 cm',
                    'phLevel': 5.2,
                    'organicMatter': 1.3,
                    'nitrogen': 32,
                    'phosphorus': 15,
                    'potassium': 120,
                    'status': 'Completed',
                    'recommendations': 'Low pH and phosphorus, apply lime and phosphate fertilizers'
                }
            ]
            
            return Response({
                'status': 'success',
                'results': mock_tests,
                'count': len(mock_tests),
                'timestamp': timezone.now().isoformat(),
                'note': 'Mock data - service unavailable'
            })


class SoilRecommendationsAPIView(APIView):
    """Soil recommendations API endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            from soil_health.models import SoilRecommendation
            
            # Get recommendations based on soil test results
            test_id = request.GET.get('test_id')
            if test_id:
                recommendations = SoilRecommendation.objects.filter(soil_test_id=test_id)
            else:
                recommendations = SoilRecommendation.objects.filter(is_active=True)[:10]
            
            results = []
            for rec in recommendations:
                results.append({
                    'id': rec.id,
                    'title': rec.title,
                    'description': rec.description,
                    'category': rec.category,
                    'priority': rec.priority,
                    'implementation': rec.implementation_steps,
                    'expectedResults': rec.expected_results,
                    'timeline': rec.implementation_timeline
                })
            
            return Response({
                'status': 'success',
                'results': results,
                'count': len(results),
                'timestamp': timezone.now().isoformat()
            })
        except Exception as e:
            # Return mock data if service fails
            mock_recommendations = [
                {
                    'id': 1,
                    'title': 'Nitrogen Application',
                    'description': 'Apply nitrogen fertilizer to improve soil fertility',
                    'category': 'Fertilization',
                    'priority': 'High',
                    'implementation': 'Apply 20kg urea per acre',
                    'expectedResults': 'Increased crop yield by 15-20%',
                    'timeline': '2-3 weeks'
                },
                {
                    'id': 2,
                    'title': 'pH Adjustment',
                    'description': 'Add lime to correct soil acidity',
                    'category': 'Soil Amendment',
                    'priority': 'Medium',
                    'implementation': 'Apply 2 tons lime per acre',
                    'expectedResults': 'Improved nutrient availability',
                    'timeline': '4-6 weeks'
                }
            ]
            
            return Response({
                'status': 'success',
                'results': mock_recommendations,
                'count': len(mock_recommendations),
                'timestamp': timezone.now().isoformat(),
                'note': 'Mock data - service unavailable'
            })


class SchemesAPIView(APIView):
    """Government schemes API endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            from schemes.models import GovernmentScheme
            
            # Get active schemes
            category = request.GET.get('category')
            if category:
                schemes = GovernmentScheme.objects.filter(
                    is_active=True,
                    category__icontains=category
                ).order_by('-created_at')
            else:
                schemes = GovernmentScheme.objects.filter(is_active=True).order_by('-created_at')
            
            results = []
            for scheme in schemes:
                results.append({
                    'id': scheme.id,
                    'title': scheme.name,
                    'description': scheme.description,
                    'category': scheme.category,
                    'benefits': scheme.scheme_amount,
                    'eligibility': scheme.eligibility_criteria,
                    'documents': scheme.required_documents,
                    'deadline': scheme.application_deadline.isoformat() if scheme.application_deadline else None,
                    'status': 'Active' if scheme.is_active else 'Inactive',
                    'isFeatured': scheme.is_featured,
                    'contact': scheme.contact_information,
                    'website': scheme.website_url,
                    'helpline': scheme.helpline_number,
                    'states': scheme.states
                })
            
            return Response({
                'status': 'success',
                'results': results,
                'count': len(results),
                'timestamp': timezone.now().isoformat()
            })
        except Exception as e:
            # Return mock data if service fails
            mock_schemes = [
                {
                    'id': 1,
                    'title': 'PM-KISAN Samman Nidhi',
                    'description': 'Direct income support of ₹6,000 per year to eligible farmer families',
                    'category': 'Income Support',
                    'benefits': '₹6,000 per year in three equal installments',
                    'eligibility': 'Small and marginal farmer families',
                    'documents': 'Land records, Bank account details, Aadhaar card',
                    'deadline': '2025-03-31T23:59:59Z',
                    'status': 'Active',
                    'isFeatured': True,
                    'contact': 'PM-KISAN Helpline: 18001155266',
                    'website': 'https://pmkisan.gov.in',
                    'helpline': '18001155266',
                    'states': 'All states and UTs'
                },
                {
                    'id': 2,
                    'title': 'Soil Health Card Scheme',
                    'description': 'Free soil testing and recommendations for farmers',
                    'category': 'Soil Health',
                    'benefits': 'Free soil testing and fertilizer recommendations',
                    'eligibility': 'All farmers with land holdings',
                    'documents': 'Land ownership documents, Aadhaar card',
                    'deadline': '2025-12-31T23:59:59Z',
                    'status': 'Active',
                    'isFeatured': False,
                    'contact': 'Department of Agriculture',
                    'website': 'https://soilhealth.dac.gov.in',
                    'helpline': '18001801551',
                    'states': 'All states and UTs'
                }
            ]
            
            return Response({
                'status': 'success',
                'results': mock_schemes,
                'count': len(mock_schemes),
                'timestamp': timezone.now().isoformat(),
                'note': 'Mock data - service unavailable'
            })


# Crops functionality removed


class MarketplaceProductsAPIView(APIView):
    """Marketplace products API endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            from marketplace.models import Product
            
            # Get active products with filtering
            category = request.GET.get('category')
            search = request.GET.get('search')
            
            products = Product.objects.filter(is_active=True)
            
            if category:
                products = products.filter(category__name__icontains=category)
            
            if search:
                products = products.filter(
                    Q(name__icontains=search) | 
                    Q(description__icontains=search)
                )
            
            products = products.order_by('-created_at')[:20]  # Limit to 20 products
            
            results = []
            for product in products:
                results.append({
                    'id': product.id,
                    'name': product.name,
                    'description': product.short_description,
                    'price': float(product.price),
                    'category': product.category.name if product.category else 'General',
                    'vendor': product.vendor.business_name if product.vendor else 'Unknown',
                    'stockQuantity': product.stock_quantity,
                    'isOrganic': product.is_organic,
                    'isCertified': product.is_certified,
                    'image': product.image.url if product.image else None,
                    'rating': float(product.rating) if product.rating else 0,
                    'reviewsCount': product.reviews.count()
                })
            
            return Response({
                'status': 'success',
                'results': results,
                'count': len(results),
                'timestamp': timezone.now().isoformat()
            })
        except Exception as e:
            # Return mock data if service fails
            mock_products = [
                {
                    'id': 1,
                    'name': 'Organic Urea Fertilizer',
                    'description': 'High-quality organic urea for better crop yield',
                    'price': 850.00,
                    'category': 'Fertilizers',
                    'vendor': 'Green Farm Solutions',
                    'stockQuantity': 100,
                    'isOrganic': True,
                    'isCertified': True,
                    'image': None,
                    'rating': 4.5,
                    'reviewsCount': 25
                },
                {
                    'id': 2,
                    'name': 'Hybrid Rice Seeds',
                    'description': 'High-yield hybrid rice seeds for better productivity',
                    'price': 1200.00,
                    'category': 'Seeds',
                    'vendor': 'AgriSeed Co.',
                    'stockQuantity': 50,
                    'isOrganic': False,
                    'isCertified': True,
                    'image': None,
                    'rating': 4.2,
                    'reviewsCount': 18
                }
            ]
            
            return Response({
                'status': 'success',
                'results': mock_products,
                'count': len(mock_products),
                'timestamp': timezone.now().isoformat(),
                'note': 'Mock data - service unavailable'
            })


class FarmerProblemsAPIView(APIView):
    """Farmer problems API endpoint"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        try:
            from farmer_problems.models import FarmerProblem
            
            # Get recent problems with filtering
            category = request.GET.get('category')
            status = request.GET.get('status')
            
            problems = FarmerProblem.objects.filter(is_active=True)
            
            if category:
                problems = problems.filter(category__name__icontains=category)
            
            if status:
                problems = problems.filter(status=status)
            
            problems = problems.order_by('-created_at')[:20]  # Limit to 20 problems
            
            results = []
            for problem in problems:
                results.append({
                    'id': problem.id,
                    'title': problem.title,
                    'description': problem.description,
                    'category': problem.category.name if problem.category else 'General',
                    'status': problem.status,
                    'farmer': problem.farmer.username if problem.farmer else 'Anonymous',
                    'location': problem.location,
                    'createdAt': problem.created_at.isoformat(),
                    'viewsCount': problem.views_count,
                    'solutionsCount': problem.solutions.count(),
                    'votesCount': problem.votes.aggregate(total=Count('vote_type'))['total'] or 0,
                    'images': [img.image.url for img in problem.images.all()] if hasattr(problem, 'images') else []
                })
            
            return Response({
                'status': 'success',
                'results': results,
                'count': len(results),
                'timestamp': timezone.now().isoformat()
            })
        except Exception as e:
            # Return mock data if service fails
            mock_problems = [
                {
                    'id': 1,
                    'title': 'Yellow leaves on rice plants',
                    'description': 'My rice plants are showing yellow leaves and slow growth',
                    'category': 'Crop Disease',
                    'status': 'Open',
                    'farmer': 'Rajesh Kumar',
                    'location': 'Hyderabad, Telangana',
                    'createdAt': '2025-01-13T10:00:00Z',
                    'viewsCount': 45,
                    'solutionsCount': 3,
                    'votesCount': 8,
                    'images': []
                },
                {
                    'id': 2,
                    'title': 'Low soil fertility',
                    'description': 'Soil in my field has become less fertile over the years',
                    'category': 'Soil Health',
                    'status': 'Open',
                    'farmer': 'Priya Sharma',
                    'location': 'Warangal, Telangana',
                    'createdAt': '2025-01-12T14:30:00Z',
                    'viewsCount': 32,
                    'solutionsCount': 5,
                    'votesCount': 12,
                    'images': []
                }
            ]
            
            return Response({
                'status': 'success',
                'results': mock_problems,
                'count': len(mock_problems),
                'timestamp': timezone.now().isoformat(),
                'note': 'Mock data - service unavailable'
            })
