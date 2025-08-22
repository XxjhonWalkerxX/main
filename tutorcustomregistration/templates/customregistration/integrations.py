"""
Integration with Open edX registration system
"""
import logging
from django.dispatch import receiver
from openedx.core.djangoapps.user_authn.signals import USER_REGISTRATION_REQUESTED
from openedx.core.djangoapps.user_api.models import UserPreference
from .models import UserCustomProfile
from .signals import save_custom_registration_data

logger = logging.getLogger(__name__)


@receiver(USER_REGISTRATION_REQUESTED)
def handle_custom_registration_fields(sender, **kwargs):
    """
    Handle custom registration fields when a user registers
    """
    user = kwargs.get('user')
    form_data = kwargs.get('form_data', {})
    
    # Extract custom fields from form data
    custom_fields = {}
    field_names = [
        'primer_apellido', 'segundo_apellido', 'numero_telefono', 
        'estado', 'municipio', 'nombre_escuela', 'cct', 'grado', 'curp'
    ]
    
    for field_name in field_names:
        if field_name in form_data:
            custom_fields[field_name] = form_data[field_name]
    
    if custom_fields and user:
        try:
            save_custom_registration_data(user, custom_fields)
            logger.info(f"Custom fields saved for user: {user.username}")
        except Exception as e:
            logger.error(f"Error saving custom fields for {user.username}: {e}")
