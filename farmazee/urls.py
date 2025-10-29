"""
URL configuration for farmazee project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from core.views import login_view, register_view, logout_view
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('admin_panel.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('signup/', register_view, name='signup'),  # Keep for backward compatibility
    path('', include('core.urls')),
    path('weather/', include('weather.urls')),
    path('marketplace/', include('marketplace.urls')),
    # Legacy 'crops' namespace compatibility to avoid NoReverseMatch in templates
    path(
        'crops/',
        include(([
            path('', core_views.crops_list, name='list'),
            path('<int:pk>/', core_views.crops_detail, name='detail'),
        ], 'crops'), namespace='crops'),
    ),
    path('schemes/', include('schemes.urls')),
    path('soil/', include('soil_health.urls')),
    path('ai-chatbot/', include('ai_chatbot.urls')),
    path('problems/', include('farmer_problems.urls')),
    path('api/', include('core.api_urls')),
    # Legacy 'community' namespace compatibility to avoid NoReverseMatch in templates
    path(
        'community/',
        include(([
            path('', core_views.community_home, name='home'),
            path('topic/<int:pk>/', core_views.community_topic_detail, name='topic_detail'),
            path('question/<int:pk>/', core_views.community_question_detail, name='question_detail'),
            path('ask/', core_views.community_ask_question, name='ask_question'),
            path('events/', core_views.community_events, name='events'),
            path('event/<int:pk>/', core_views.community_event_detail, name='event_detail'),
        ], 'community'), namespace='community'),
    ),
]

# Custom error handlers
handler404 = 'core.error_handling.custom_404_handler'
handler500 = 'core.error_handling.custom_500_handler'
handler403 = 'core.error_handling.custom_403_handler'
handler400 = 'core.error_handling.custom_400_handler'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
else:
    # Serve static files in production
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin site customization
admin.site.site_header = "Farmazee Admin"
admin.site.site_title = "Farmazee Admin Portal"
admin.site.index_title = "Welcome to Farmazee Administration"

