"""
URLs for Farmer Problems app
"""

from django.urls import path
from . import views

app_name = 'farmer_problems'

urlpatterns = [
    path('', views.problem_list, name='list'),
    path('create/', views.problem_create, name='create'),
    path('categories/', views.category_list, name='categories'),
    path('experts/', views.expert_list, name='experts'),
    path('become-expert/', views.become_expert, name='become_expert'),
    path('vote/', views.vote, name='vote'),
    path('solution/<int:solution_id>/accept/', views.accept_solution, name='accept_solution'),
    path('<slug:slug>/', views.problem_detail, name='detail'),
    path('<slug:problem_slug>/solution/add/', views.solution_create, name='solution_create'),
]

