"""
Advanced Celery configuration for Farmazee Enterprise Platform.

This module configures Celery for background task processing,
distributed computing, and advanced task scheduling.
"""

import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmazee.settings')

# Create the Celery app
app = Celery('farmazee')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Advanced Celery Configuration
app.conf.update(
    # Task routing
    task_routes={
        'ai_ml.tasks.*': {'queue': 'ai_ml'},
        'weather.tasks.*': {'queue': 'weather'},
        'analytics.tasks.*': {'queue': 'analytics'},
        'marketplace.tasks.*': {'queue': 'marketplace'},
        'notifications.tasks.*': {'queue': 'notifications'},
    },
    
    # Task serialization
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Task execution
    task_always_eager=settings.DEBUG,
    task_eager_propagates=settings.DEBUG,
    
    # Worker configuration
    worker_max_tasks_per_child=1000,
    worker_prefetch_multiplier=1,
    worker_disable_rate_limits=False,
    
    # Result backend
    result_backend='django-db',
    result_expires=3600,  # 1 hour
    
    # Task time limits
    task_soft_time_limit=300,  # 5 minutes
    task_time_limit=600,       # 10 minutes
    
    # Beat schedule (periodic tasks)
    beat_schedule={
        # Weather data updates every 30 minutes
        'update-weather-data': {
            'task': 'weather.tasks.update_weather_data',
            'schedule': crontab(minute='*/30'),
            'options': {'queue': 'weather'}
        },
        
        # Crop monitoring every hour
        'monitor-crops': {
            'task': 'crops.tasks.monitor_crop_health',
            'schedule': crontab(minute=0, hour='*/1'),
            'options': {'queue': 'ai_ml'}
        },
        
        # Market price updates every 2 hours
        'update-market-prices': {
            'task': 'marketplace.tasks.update_market_prices',
            'schedule': crontab(minute=0, hour='*/2'),
            'options': {'queue': 'marketplace'}
        },
        
        # Analytics processing daily at 2 AM
        'process-analytics': {
            'task': 'analytics.tasks.process_daily_analytics',
            'schedule': crontab(minute=0, hour=2),
            'options': {'queue': 'analytics'}
        },
        
        # AI model retraining weekly on Sunday at 3 AM
        'retrain-ai-models': {
            'task': 'ai_ml.tasks.retrain_models',
            'schedule': crontab(minute=0, hour=3, day_of_week=0),
            'options': {'queue': 'ai_ml'}
        },
        
        # Database cleanup monthly
        'cleanup-database': {
            'task': 'core.tasks.cleanup_old_data',
            'schedule': crontab(minute=0, hour=4, day_of_month=1),
            'options': {'queue': 'maintenance'}
        },
        
        # Health check every 5 minutes
        'health-check': {
            'task': 'core.tasks.system_health_check',
            'schedule': crontab(minute='*/5'),
            'options': {'queue': 'monitoring'}
        },
    },
    
    # Task routing
    task_default_queue='default',
    task_default_exchange='farmazee',
    task_default_routing_key='farmazee.default',
    
    # Worker pool
    worker_pool='prefork',
    worker_concurrency=4,
    
    # Task compression
    task_compression='gzip',
    result_compression='gzip',
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Security
    worker_hijack_root_logger=False,
    worker_log_color=True,
    
    # Error handling
    task_reject_on_worker_lost=True,
    task_acks_late=True,
    
    # Performance
    worker_disable_rate_limits=False,
    worker_max_memory_per_child=200000,  # 200MB
)

# Task annotations for specific tasks
app.conf.task_annotations = {
    'ai_ml.tasks.train_model': {
        'rate_limit': '10/m',
        'time_limit': 3600,  # 1 hour
        'soft_time_limit': 3300,  # 55 minutes
    },
    'weather.tasks.fetch_weather_data': {
        'rate_limit': '100/m',
        'time_limit': 300,  # 5 minutes
    },
    'analytics.tasks.process_large_dataset': {
        'rate_limit': '5/m',
        'time_limit': 1800,  # 30 minutes
    },
}

@app.task(bind=True)
def debug_task(self):
    """Debug task to test Celery configuration."""
    print(f'Request: {self.request!r}')

# Import tasks to ensure they are registered
from ai_ml import tasks as ai_ml_tasks
from weather import tasks as weather_tasks
from analytics import tasks as analytics_tasks
from marketplace import tasks as marketplace_tasks
from core import tasks as core_tasks

