from django.urls import path
from . import views

app_name = 'soil_health'

urlpatterns = [
    path('', views.soil_home, name='home'),
    path('tips/', views.tip_list, name='tips'),
    path('tip/<int:pk>/', views.tip_detail, name='tip_detail'),
    path('tests/', views.soil_test_list, name='tests'),
    path('test/<int:pk>/', views.soil_test_detail, name='test_detail'),
    path('records/', views.soil_health_record, name='records'),
    path('improvements/', views.soil_improvement_list, name='improvements'),
    path('conservation/', views.soil_conservation_list, name='conservation'),
    path('monitoring/', views.soil_monitoring_schedule, name='monitoring'),
    path('alerts/', views.soil_health_alerts, name='alerts'),
    path('soil-types/', views.soil_type_list, name='soil_types'),
    path('soil-type/<int:pk>/', views.soil_type_detail, name='soil_type_detail'),
    path('recommendations/', views.soil_recommendations, name='recommendations'),
    path('monitoring-dashboard/', views.soil_monitoring, name='monitoring'),
    path('schedule-test/', views.schedule_soil_test, name='schedule_test'),
]
