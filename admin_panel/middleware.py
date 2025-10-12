from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout

class AdminPanelMiddleware:
    """
    Middleware to handle admin panel access and maintenance mode
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if user is trying to access admin panel
        if request.path.startswith('/admin-panel/'):
            # Allow access to login page
            if request.path == '/admin-panel/':
                response = self.get_response(request)
                return response
            
            # Check if user is authenticated and has admin privileges
            if not request.user.is_authenticated:
                return redirect('login')
            
            if not (request.user.is_staff or request.user.is_superuser):
                return redirect('core:home')
        
        response = self.get_response(request)
        return response
from django.urls import reverse
from django.contrib.auth import logout

class AdminPanelMiddleware:
    """
    Middleware to handle admin panel access and maintenance mode
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if user is trying to access admin panel
        if request.path.startswith('/admin-panel/'):
            # Allow access to login page
            if request.path == '/admin-panel/':
                response = self.get_response(request)
                return response
            
            # Check if user is authenticated and has admin privileges
            if not request.user.is_authenticated:
                return redirect('login')
            
            if not (request.user.is_staff or request.user.is_superuser):
                return redirect('core:home')
        
        response = self.get_response(request)
        return response
