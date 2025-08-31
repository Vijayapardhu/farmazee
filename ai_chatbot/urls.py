from django.urls import path
from . import views

app_name = 'ai_chatbot'

urlpatterns = [
    path('', views.ai_chat_home, name='home'),
    path('chat/', views.chat_interface, name='chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('history/', views.chat_history, name='history'),
    path('analytics/', views.query_analytics, name='analytics'),
    path('rate-response/', views.rate_response, name='rate_response'),
]
