from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.weather_home, name='home'),
    path('dashboard/', views.weather_dashboard, name='dashboard'),
    path('detail/<str:location>/', views.weather_detail, name='detail'),
    path('alerts/', views.weather_alerts, name='alerts'),
    path('forecast/', views.weather_forecast, name='forecast'),
    path('api/<str:location>/', views.weather_api, name='api'),
    path('api/<str:location>/forecast/', views.forecast_api, name='forecast_api'),
    # Live weather API endpoints
    path('api/update/', views.update_weather_data, name='update_weather'),
    path('api/live/', views.get_live_weather_api, name='live_weather'),
]
