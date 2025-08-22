"""
Simple middleware to handle custom registration fields
without requiring a separate Django app
"""
import json
import re
import logging
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.db import transaction
from openedx.core.djangoapps.user_api.accounts.api import create_account
from openedx.core.djangoapps.user_authn.views.registration_form import RegistrationView
from student.models import UserProfile

User = get_user_model()
logger = logging.getLogger(__name__)

class CustomRegistrationMiddleware:
    """Middleware to process custom Mexican registration fields"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        # Process request before view
        if self._should_process_registration(request):
            validation_response = self._validate_custom_fields_only(request)
            if validation_response:
                return validation_response
            
            # Store custom data for post-processing
            request.custom_registration_data = self._extract_custom_fields(request)
            
        response = self.get_response(request)
        
        # Process after successful registration
        if (self._should_process_registration(request) and 
            hasattr(request, 'custom_registration_data') and 
            response.status_code == 200):
            self._save_custom_profile_data(request, response)
            
        return response
    
    def _should_process_registration(self, request):
        """Check if this is a registration request with custom fields"""
        return (
            request.method == 'POST' and 
            '/api/user/v2/account/registration/' in request.path and
            self._has_custom_fields(request)
        )
    
    def _has_custom_fields(self, request):
        """Check if request contains our custom Mexican fields"""
        custom_fields = ['primer_apellido', 'segundo_apellido', 'numero_telefono', 
                        'estado', 'municipio', 'nombre_escuela', 'cct', 'grado', 'curp']
        
        for field in custom_fields:
            if field in request.POST:
                return True
        return False
    
    def _validate_custom_fields_only(self, request):
        """Validate custom fields and return error response if invalid"""
        try:
            custom_data = self._extract_custom_fields(request)
            logger.info(f"🔍 Validating custom fields: {custom_data}")
            
            validation_errors = self._validate_custom_fields(custom_data)
            
            if validation_errors:
                logger.warning(f"❌ Validation errors: {validation_errors}")
                return JsonResponse({
                    'success': False,
                    'field_errors': validation_errors,
                    'message': 'Errores de validación en campos personalizados'
                }, status=400)
            
            logger.info(f"✅ Custom fields validation passed for {len(custom_data)} fields")
            return None
            
        except Exception as e:
            logger.error(f"💥 Error validating custom fields: {e}", exc_info=True)
            return JsonResponse({
                'success': False,
                'error': 'Error validando campos personalizados'
            }, status=500)
    
    def _save_custom_profile_data(self, request, response):
        """Save custom data to user profile after successful registration"""
        try:
            if not hasattr(request, 'custom_registration_data'):
                logger.warning("❌ No custom registration data found in request")
                return
                
            # Extract username from response or request
            username = request.POST.get('username', '')
            if not username:
                logger.warning("❌ No username found in request")
                return
                
            logger.info(f"💾 Attempting to save custom data for user: {username}")
                
            # Find the user
            try:
                user = User.objects.get(username=username)
                profile, created = UserProfile.objects.get_or_create(user=user)
                
                logger.info(f"👤 Found user {username}, profile created: {created}")
                
                # Get existing meta or create new
                meta = profile.meta if profile.meta else {}
                
                # Add custom Mexican fields to meta
                custom_data = request.custom_registration_data
                for field, value in custom_data.items():
                    meta[field] = value
                    
                # Save updated profile
                profile.meta = meta
                profile.save()
                
                logger.info(f"✅ Saved custom profile data for user {username}: {list(custom_data.keys())}")
                
            except User.DoesNotExist:
                logger.error(f"❌ User {username} not found after registration")
            except Exception as e:
                logger.error(f"💥 Error saving profile data for {username}: {e}", exc_info=True)
                
        except Exception as e:
            logger.error(f"💥 Error in _save_custom_profile_data: {e}", exc_info=True)
    
    def _process_custom_registration(self, request):
        """Legacy method - now split into validation and saving"""
        return self._validate_custom_fields_only(request)
    
    def _extract_custom_fields(self, request):
        """Extract custom fields from request"""
        custom_data = {}
        fields = ['primer_apellido', 'segundo_apellido', 'numero_telefono', 
                 'estado', 'municipio', 'nombre_escuela', 'cct', 'grado', 'curp']
        
        for field in fields:
            value = request.POST.get(field, '').strip()
            if value:
                # Handle list values (Django forms sometimes send as lists)
                if isinstance(value, list):
                    custom_data[field] = value[0] if value else ''
                else:
                    custom_data[field] = value
                    
        return custom_data
    
    def _validate_custom_fields(self, data):
        """Validate custom Mexican fields - MODO PERMISIVO PARA PRUEBAS"""
        errors = {}
        
        # CURP validation - MÁS PERMISIVO
        if 'curp' in data and data['curp']:
            curp = data['curp'].strip()
            if len(curp) < 10 or len(curp) > 20:  # Rango más amplio
                errors['curp'] = f'El CURP debe tener entre 10-20 caracteres (recibido: {len(curp)})'
        
        # CCT validation - MÁS PERMISIVO  
        if 'cct' in data and data['cct']:
            cct = data['cct'].strip()
            if len(cct) < 5 or len(cct) > 15:  # Rango más amplio
                errors['cct'] = f'La CCT debe tener entre 5-15 caracteres (recibido: {len(cct)})'
                
        # Phone validation - MÁS PERMISIVO
        if 'numero_telefono' in data and data['numero_telefono']:
            phone = data['numero_telefono'].strip()
            clean_phone = re.sub(r'[^0-9]', '', phone)
            if len(clean_phone) < 8 or len(clean_phone) > 12:  # Rango más amplio
                errors['numero_telefono'] = f'El teléfono debe tener entre 8-12 dígitos (recibido: {len(clean_phone)})'
        
        # Required field validation - SOLO CAMPOS CRÍTICOS
        required_fields = ['primer_apellido', 'numero_telefono']  # Reducido a los esenciales
        
        for field in required_fields:
            if field not in data or not data[field] or not data[field].strip():
                errors[field] = f'El campo {field.replace("_", " ")} es obligatorio'
                
        return errors
    
    def _validate_curp(self, curp):
        """Validate Mexican CURP format"""
        if not curp or len(curp) != 18:
            return False
        pattern = r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9]{2}$'
        return bool(re.match(pattern, curp.upper()))
    
    def _validate_cct(self, cct):
        """Validate Mexican CCT format"""
        if not cct or len(cct) != 10:
            return False
        pattern = r'^[0-9]{2}[A-Z]{3}[0-9]{4}[A-Z]$'
        return bool(re.match(pattern, cct.upper()))
        
    def _validate_phone(self, phone):
        """Validate Mexican phone number"""
        if not phone:
            return False
        # Remove any non-digit characters
        clean_phone = re.sub(r'[^0-9]', '', phone)
        return len(clean_phone) == 10
