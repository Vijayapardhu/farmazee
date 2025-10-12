from django.urls import path
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'profiles', api_views.UserProfileViewSet)
router.register(r'notifications', api_views.NotificationViewSet, basename='notification')
router.register(r'faqs', api_views.FAQViewSet)
router.register(r'contact', api_views.ContactViewSet)

urlpatterns = router.urls + [
    path('search/', api_views.SearchAPIView.as_view(), name='api-search'),
    path('stats/', api_views.StatsAPIView.as_view(), name='api-stats'),
    path('weather/current/', api_views.WeatherAPIView.as_view(), name='api-weather-current'),
    path('marketplace/prices/', api_views.MarketplacePricesAPIView.as_view(), name='api-marketplace-prices'),
]
