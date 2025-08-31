from django.urls import path
from . import views

app_name = 'crops'

urlpatterns = [
    path('', views.crop_list, name='list'),
    path('<int:pk>/', views.crop_detail, name='detail'),
    path('<int:pk>/plan/', views.crop_plan, name='plan'),
    path('<int:pk>/activities/', views.crop_activities, name='activities'),
    path('<int:pk>/monitoring/', views.crop_monitoring, name='monitoring'),
    path('<int:pk>/yield-tracking/', views.crop_yield_tracking, name='yield_tracking'),
    path('calendar/', views.crop_calendar, name='calendar'),
    path('pest-diseases/', views.pest_disease_list, name='pest_diseases'),
    path('advice/', views.crop_advice, name='advice'),
    path('my-crops/', views.my_crops, name='my_crops'),
]
