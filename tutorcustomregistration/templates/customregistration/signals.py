"""
Django signals to handle user registration with custom fields
"""
import logging
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from .models import UserCustomProfile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_custom_profile(sender, instance, created, **kwargs):
    """
    Create a custom profile when a new user is registered
    This signal is triggered after a User instance is saved
    """
    if created:
        logger.info(f"New user created: {instance.username}")
        # Note: The custom profile will be created by the registration view
        # This signal is here for future enhancements


def save_custom_registration_data(user, custom_data):
    """
    Save custom registration data for a user
    
    Args:
        user: User instance
        custom_data: Dictionary with custom field data
    """
    try:
        # Check if profile already exists
        profile, created = UserCustomProfile.objects.get_or_create(
            user=user,
            defaults={
                'primer_apellido': custom_data.get('primer_apellido', ''),
                'segundo_apellido': custom_data.get('segundo_apellido', ''),
                'numero_telefono': custom_data.get('numero_telefono', ''),
                'estado': custom_data.get('estado', ''),
                'municipio': custom_data.get('municipio', ''),
                'nombre_escuela': custom_data.get('nombre_escuela', ''),
                'cct': custom_data.get('cct', ''),
                'grado': custom_data.get('grado', ''),
                'curp': custom_data.get('curp', ''),
            }
        )
        
        if created:
            logger.info(f"Custom profile created for user: {user.username}")
        else:
            # Update existing profile
            for field, value in custom_data.items():
                if hasattr(profile, field):
                    setattr(profile, field, value)
            profile.save()
            logger.info(f"Custom profile updated for user: {user.username}")
            
        return profile
        
    except ValidationError as e:
        logger.error(f"Validation error creating custom profile for {user.username}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error creating custom profile for {user.username}: {e}")
        raise
