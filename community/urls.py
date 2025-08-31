from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_home, name='home'),
    path('forum/', views.forum_list, name='forum'),
    path('forum/<int:pk>/', views.forum_detail, name='forum_detail'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('qa/', views.qa_list, name='qa'),
    path('qa/<int:pk>/', views.qa_detail, name='qa_detail'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('ask-question/', views.ask_question, name='ask_question'),
    path('experts/', views.expert_list, name='experts'),
    path('expert/<int:pk>/', views.expert_detail, name='expert_detail'),
    path('events/', views.event_list, name='events'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('topics/', views.topics_list, name='topics'),
    path('questions/', views.questions_list, name='questions'),
]
