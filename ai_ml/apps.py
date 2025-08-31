"""
AI/ML Application Configuration for Farmazee Enterprise Platform.
"""

from django.apps import AppConfig


class AiMlConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ai_ml'
    verbose_name = 'AI/ML Services'
    
    def ready(self):
        """Initialize AI/ML services when Django starts."""
        try:
            import ai_ml.signals
            import ai_ml.tasks
        except ImportError:
            pass

