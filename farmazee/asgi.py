"""
Advanced ASGI config for Farmazee Enterprise Platform.

It exposes the ASGI callable as a module-level variable named ``application``.
Supports WebSocket, HTTP, and real-time communication.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmazee.settings')

# Initialize Django
django.setup()

# Import routing after Django setup
from core.routing import websocket_urlpatterns

# ASGI application
application = ProtocolTypeRouter({
    # HTTP requests are handled by Django
    "http": get_asgi_application(),
    
    # WebSocket requests are handled by Channels
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
