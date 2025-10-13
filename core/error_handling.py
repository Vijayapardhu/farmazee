"""
Custom error handling for Farmazee
"""

import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import traceback
import sys

logger = logging.getLogger(__name__)


def custom_404_handler(request, exception):
    """Custom 404 error handler"""
    logger.warning(f"404 Error: {request.path} - {request.META.get('HTTP_USER_AGENT', 'Unknown')}")
    
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Not Found',
            'message': 'The requested resource was not found.',
            'status': 404
        }, status=404)
    
    return render(request, 'errors/404.html', status=404)


def custom_500_handler(request):
    """Custom 500 error handler"""
    logger.error(f"500 Error: {request.path} - {traceback.format_exc()}")
    
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred. Please try again later.',
            'status': 500
        }, status=500)
    
    return render(request, 'errors/500.html', status=500)


def custom_403_handler(request, exception):
    """Custom 403 error handler"""
    logger.warning(f"403 Error: {request.path} - {request.user}")
    
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource.',
            'status': 403
        }, status=403)
    
    return render(request, 'errors/403.html', status=403)


def custom_400_handler(request, exception):
    """Custom 400 error handler"""
    logger.warning(f"400 Error: {request.path} - {exception}")
    
    if request.path.startswith('/api/'):
        return JsonResponse({
            'error': 'Bad Request',
            'message': 'The request was invalid or cannot be served.',
            'status': 400
        }, status=400)
    
    return render(request, 'errors/400.html', status=400)


class ErrorHandlingMiddleware:
    """Middleware to handle errors gracefully"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_exception(self, request, exception):
        """Handle unhandled exceptions"""
        logger.error(f"Unhandled Exception: {request.path} - {exception}")
        logger.error(traceback.format_exc())
        
        # Don't handle exceptions in debug mode
        if settings.DEBUG:
            return None
        
        if request.path.startswith('/api/'):
            return JsonResponse({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred. Please try again later.',
                'status': 500
            }, status=500)
        
        return render(request, 'errors/500.html', status=500)


def log_api_error(request, error, status_code=500):
    """Log API errors with context"""
    logger.error(f"API Error {status_code}: {request.path}")
    logger.error(f"Method: {request.method}")
    logger.error(f"User: {getattr(request, 'user', 'Anonymous')}")
    logger.error(f"Error: {error}")
    logger.error(f"Traceback: {traceback.format_exc()}")


def handle_validation_error(errors):
    """Handle form validation errors"""
    error_list = []
    for field, field_errors in errors.items():
        if isinstance(field_errors, list):
            for error in field_errors:
                error_list.append(f"{field}: {error}")
        else:
            error_list.append(f"{field}: {field_errors}")
    
    return {
        'error': 'Validation Error',
        'message': 'Please correct the following errors:',
        'details': error_list
    }


def safe_json_response(data, status=200):
    """Safely create JSON response with error handling"""
    try:
        return JsonResponse(data, status=status)
    except Exception as e:
        logger.error(f"Error creating JSON response: {e}")
        return JsonResponse({
            'error': 'Response Error',
            'message': 'Unable to process response'
        }, status=500)


def log_user_action(user, action, details=None):
    """Log user actions for debugging"""
    logger.info(f"User Action: {user} - {action}")
    if details:
        logger.info(f"Details: {details}")


def log_performance_issue(request, duration, threshold=2.0):
    """Log performance issues"""
    if duration > threshold:
        logger.warning(f"Slow Request: {request.path} took {duration:.2f}s")
        logger.warning(f"Method: {request.method}")
        logger.warning(f"User: {getattr(request, 'user', 'Anonymous')}")


# Error context for templates
def get_error_context(request, error_code, error_message=None):
    """Get context for error pages"""
    context = {
        'error_code': error_code,
        'error_message': error_message or f'Error {error_code}',
        'request_path': request.path,
        'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown'),
        'timestamp': request.META.get('REQUEST_TIME', None),
    }
    
    # Add user information if available
    if hasattr(request, 'user') and request.user.is_authenticated:
        context['user'] = request.user
    
    return context


# API Error Decorators
def api_error_handler(view_func):
    """Decorator to handle API errors"""
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            log_api_error(request, e)
            return safe_json_response({
                'error': 'Internal Server Error',
                'message': 'An unexpected error occurred'
            }, status=500)
    return wrapper


def require_api_key(view_func):
    """Decorator to require API key for certain endpoints"""
    def wrapper(request, *args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != settings.API_KEY:
            return safe_json_response({
                'error': 'Unauthorized',
                'message': 'Valid API key required'
            }, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper


# Error Recovery Functions
def recover_from_database_error(func, *args, **kwargs):
    """Attempt to recover from database errors"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Database error in {func.__name__}: {e}")
        # Attempt recovery or return default value
        return None


def recover_from_api_error(url, timeout=10):
    """Attempt to recover from external API errors"""
    try:
        import requests
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"API error for {url}: {e}")
        return None

