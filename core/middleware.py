"""
Custom middleware for handling ngrok domains and other dynamic host configurations.
"""

import re
from django.conf import settings


class NgrokHostMiddleware:
    """
    Middleware to automatically allow ngrok domains and prevent DisallowedHost errors.
    This is useful for development and testing with ngrok tunnels.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Check if the host is an ngrok domain
        host = request.get_host()
        
        # Pattern to match ngrok-free.app domains
        ngrok_pattern = r'^[a-f0-9]+\.ngrok-free\.app$'
        
        if re.match(ngrok_pattern, host):
            # Add the host to ALLOWED_HOSTS if it's not already there
            if host not in settings.ALLOWED_HOSTS:
                settings.ALLOWED_HOSTS.append(host)
                
            # Also add to CORS settings if needed
            if hasattr(settings, 'CORS_ALLOWED_ORIGINS'):
                https_url = f"https://{host}"
                if https_url not in settings.CORS_ALLOWED_ORIGINS:
                    settings.CORS_ALLOWED_ORIGINS.append(https_url)
                    
            # Add to CSRF trusted origins
            if hasattr(settings, 'CSRF_TRUSTED_ORIGINS'):
                if https_url not in settings.CSRF_TRUSTED_ORIGINS:
                    settings.CSRF_TRUSTED_ORIGINS.append(https_url)
        
        response = self.get_response(request)
        return response
