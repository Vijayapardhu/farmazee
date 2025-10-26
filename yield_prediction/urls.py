from django.urls import path
from . import views

app_name = 'yield_prediction'

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict_yield, name='predict_yield'),
    path('recommendations/', views.crop_recommendations, name='crop_recommendations'),
    path('predictions/<int:prediction_id>/', views.prediction_detail, name='prediction_detail'),
    path('predictions/', views.prediction_list, name='prediction_list'),
    path('predictions/<int:prediction_id>/history/add/', views.add_yield_history, name='add_yield_history'),
]


