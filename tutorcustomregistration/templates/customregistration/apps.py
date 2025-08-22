"""
Django app for custom registration fields
"""
from django.apps import AppConfig

class CustomRegistrationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customregistration'
    verbose_name = 'Custom Registration Fields'

    def ready(self):
        # Import signals here to avoid circular imports
        from . import signals
        from . import integrations
