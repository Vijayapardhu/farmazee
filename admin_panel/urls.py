from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Dashboard
    path('', views.admin_dashboard, name='dashboard'),
    
    # User Management
    path('users/', views.user_management, name='user_management'),
    path('users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('users/<int:user_id>/toggle-status/', views.toggle_user_status, name='toggle_user_status'),
    
    # Knowledge Base Management
    path('knowledge-base/', views.knowledge_base_management, name='knowledge_base'),
    path('knowledge-base/add/', views.add_knowledge_item, name='add_knowledge'),
    path('knowledge-base/<int:item_id>/edit/', views.edit_knowledge_item, name='edit_knowledge'),
    path('knowledge-base/<int:item_id>/delete/', views.delete_knowledge_item, name='delete_knowledge'),
    
    # Farmer Problems Management
    path('farmer-problems/', views.farmer_problems_management, name='farmer_problems'),
    path('farmer-problems/<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('farmer-problems/<int:problem_id>/mark-solved/', views.mark_problem_solved, name='mark_problem_solved'),
    path('farmer-problems/<int:problem_id>/delete/', views.delete_problem, name='delete_problem'),
    path('solutions/<int:solution_id>/accept/', views.accept_solution, name='accept_solution'),
    path('solutions/<int:solution_id>/delete/', views.delete_solution, name='delete_solution'),
    
    # Analytics
    path('analytics/', views.analytics_dashboard, name='analytics'),
    
    # System Settings
    path('settings/', views.system_settings, name='system_settings'),
    
    # Data Export
    path('export/', views.export_data, name='export_data'),
    
    # Advanced Admin Features
    path('bulk-user-actions/', views.bulk_user_actions, name='bulk_user_actions'),
    path('content-moderation/', views.content_moderation, name='content_moderation'),
    path('approve-content/<str:content_type>/<int:content_id>/', views.approve_content, name='approve_content'),
    path('delete-content/<str:content_type>/<int:content_id>/', views.delete_content, name='delete_content'),
    path('advanced-analytics/', views.advanced_analytics, name='advanced_analytics'),
    path('activity-logs/', views.activity_logs, name='activity_logs'),
    path('broadcast-notification/', views.broadcast_notification, name='broadcast_notification'),
    path('database-management/', views.database_management, name='database_management'),
    path('expert-verification/', views.expert_verification, name='expert_verification'),
    path('verify-expert/<int:expert_id>/', views.verify_expert, name='verify_expert'),
    path('reject-expert/<int:expert_id>/', views.reject_expert, name='reject_expert'),
    path('platform-statistics/', views.platform_statistics, name='platform_statistics'),
    
    # User Features Management
    path('schemes/', views.schemes_management, name='schemes_management'),
    path('schemes/add/', views.add_scheme, name='add_scheme'),
    path('schemes/<int:scheme_id>/edit/', views.edit_scheme, name='edit_scheme'),
    path('schemes/<int:scheme_id>/delete/', views.delete_scheme, name='delete_scheme'),
    path('schemes/<int:scheme_id>/toggle-status/', views.toggle_scheme_status, name='toggle_scheme_status'),
    path('crops/', views.crops_management, name='crops_management'),
    path('marketplace/', views.marketplace_management, name='marketplace_management'),
    path('soil-tests/', views.soil_tests_management, name='soil_tests_management'),
    path('community/', views.community_management, name='community_management'),
]
