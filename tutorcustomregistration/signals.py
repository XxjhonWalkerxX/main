"""
Django signals to handle custom registration fields
This approach works without requiring middleware or custom apps
"""
import re
import json
import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from student.models import UserProfile

User = get_user_model()
logger = logging.getLogger(__name__)

class CustomRegistrationHandler:
    """Handler for custom Mexican registration fields"""
    
    @staticmethod
    def validate_mexican_fields(data):
        """Validate Mexican-specific fields"""
        errors = {}
        
        # CURP validation
        if 'curp' in data and data['curp']:
            if not CustomRegistrationHandler._validate_curp(data['curp']):
                errors['curp'] = 'El CURP debe tener formato válido mexicano (18 caracteres)'
        
        # CCT validation
        if 'cct' in data and data['cct']:
            if not CustomRegistrationHandler._validate_cct(data['cct']):
                errors['cct'] = 'La CCT debe tener formato válido (10 caracteres)'
                
        # Phone validation
        if 'numero_telefono' in data and data['numero_telefono']:
            if not CustomRegistrationHandler._validate_phone(data['numero_telefono']):
                errors['numero_telefono'] = 'El teléfono debe tener exactamente 10 dígitos'
        
        # Required fields
        required_fields = ['primer_apellido', 'numero_telefono', 'estado', 
                          'municipio', 'nombre_escuela', 'cct', 'grado', 'curp']
        
        for field in required_fields:
            if field not in data or not data[field] or not str(data[field]).strip():
                errors[field] = f'El campo {field.replace("_", " ")} es obligatorio'
                
        return errors
    
    @staticmethod
    def _validate_curp(curp):
        """Validate Mexican CURP format"""
        if not curp or len(curp) != 18:
            return False
        pattern = r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9]{2}$'
        return bool(re.match(pattern, curp.upper()))
    
    @staticmethod
    def _validate_cct(cct):
        """Validate Mexican CCT format"""
        if not cct or len(cct) != 10:
            return False
        pattern = r'^[0-9]{2}[A-Z]{3}[0-9]{4}[A-Z]$'
        return bool(re.match(pattern, cct.upper()))
        
    @staticmethod
    def _validate_phone(phone):
        """Validate Mexican phone number"""
        if not phone:
            return False
        clean_phone = re.sub(r'[^0-9]', '', str(phone))
        return len(clean_phone) == 10

    @staticmethod
    def save_custom_profile_data(user, custom_data):
        """Save custom data to user profile"""
        try:
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Get existing meta or create new
            meta = profile.meta if profile.meta else {}
            
            # Add custom Mexican fields to meta
            for field, value in custom_data.items():
                if value:  # Only save non-empty values
                    meta[field] = str(value).strip()
                    
            # Save updated profile
            profile.meta = meta
            profile.save()
            
            logger.info(f"✅ Saved custom profile data for user {user.username}: {list(custom_data.keys())}")
            return True
            
        except Exception as e:
            logger.error(f"💥 Error saving profile data for {user.username}: {e}")
            return False

# Signal to handle user registration
@receiver(post_save, sender=User)
def handle_custom_registration(sender, instance, created, **kwargs):
    """Handle custom registration data after user is created"""
    if created:  # Only for new users
        logger.info(f"🔍 New user created: {instance.username}")
        
        # Check if we have custom registration data stored somewhere
        # This would need to be passed from the registration view
        # For now, we'll log that a new user was created
        logger.info(f"📝 User {instance.username} ready for custom data processing")

# Registration view wrapper (if needed)
def process_registration_with_custom_fields(request, registration_data):
    """Process registration with custom field validation"""
    try:
        # Extract custom fields
        custom_fields = ['primer_apellido', 'segundo_apellido', 'numero_telefono', 
                        'estado', 'municipio', 'nombre_escuela', 'cct', 'grado', 'curp']
        
        custom_data = {}
        for field in custom_fields:
            value = registration_data.get(field)
            if value:
                custom_data[field] = value
        
        if custom_data:
            # Validate custom fields
            validation_errors = CustomRegistrationHandler.validate_mexican_fields(custom_data)
            
            if validation_errors:
                logger.warning(f"❌ Custom field validation errors: {validation_errors}")
                return {'success': False, 'field_errors': validation_errors}
            
            logger.info(f"✅ Custom fields validated successfully: {list(custom_data.keys())}")
            return {'success': True, 'custom_data': custom_data}
        
        return {'success': True, 'custom_data': {}}
        
    except Exception as e:
        logger.error(f"💥 Error processing custom registration: {e}")
        return {'success': False, 'error': str(e)}
