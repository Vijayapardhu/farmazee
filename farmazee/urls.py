"""
URL configuration for farmazee project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from core.views import signup

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-panel/', include('admin_panel.urls')),
    path('accounts/', include('allauth.urls')),
    path('signup/', signup, name='signup'),
    # Redirect users/register/ to signup/ for compatibility
    path('users/register/', RedirectView.as_view(url='/signup/', permanent=False), name='users_register'),
    path('', include('core.urls')),
    path('weather/', include('weather.urls')),
    path('crops/', include('crops.urls')),
    path('marketplace/', include('marketplace.urls')),
    path('community/', include('community.urls')),
    path('schemes/', include('schemes.urls')),
    path('soil/', include('soil_health.urls')),
    path('ai-chatbot/', include('ai_chatbot.urls')),
    path('problems/', include('farmer_problems.urls')),
    path('api/', include('core.api_urls')),
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

