from django.urls import path
from . import views

app_name = 'schemes'

urlpatterns = [
    path('', views.scheme_list, name='list'),
    path('<int:pk>/', views.scheme_detail, name='detail'),
    path('apply/<int:pk>/', views.scheme_apply, name='apply'),
    path('applications/', views.application_list, name='applications'),
    path('dashboard/', views.scheme_dashboard, name='dashboard'),
    path('eligibility/', views.scheme_eligibility, name='eligibility'),
    path('calculator/', views.scheme_calculator, name='calculator'),
    path('guidelines/', views.scheme_guidelines, name='guidelines'),
]
