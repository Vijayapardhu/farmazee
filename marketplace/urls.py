from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.marketplace_home, name='home'),
    path('products/', views.product_list, name='products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('category/<int:pk>/', views.category_products, name='category_products'),
    path('orders/', views.order_list, name='orders'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('vendor/', views.vendor_dashboard, name='vendor_dashboard'),
    path('inputs/', views.input_list, name='inputs'),
    path('input/<int:pk>/', views.input_detail, name='input_detail'),
    path('input-category/<int:pk>/', views.input_category, name='input_category'),
]
