"""
Custom registration views to handle extended user registration
"""
import json
import logging
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from openedx.core.djangoapps.user_authn.views.registration_form import RegistrationView
from .models import UserCustomProfile
from .signals import save_custom_registration_data

logger = logging.getLogger(__name__)


class CustomRegistrationView(RegistrationView):
    """
    Extended registration view that handles custom fields
    """
    
    def post(self, request):
        """
        Handle POST request with custom fields
        """
        # Extract custom fields from request
        custom_fields = {
            'primer_apellido': request.POST.get('primer_apellido', ''),
            'segundo_apellido': request.POST.get('segundo_apellido', ''),
            'numero_telefono': request.POST.get('numero_telefono', ''),
            'estado': request.POST.get('estado', ''),
            'municipio': request.POST.get('municipio', ''),
            'nombre_escuela': request.POST.get('nombre_escuela', ''),
            'cct': request.POST.get('cct', ''),
            'grado': request.POST.get('grado', ''),
            'curp': request.POST.get('curp', ''),
        }
        
        logger.info(f"Registration attempt with custom fields: {list(custom_fields.keys())}")
        
        # Validate CURP uniqueness before proceeding
        curp = custom_fields.get('curp', '').upper()
        if curp and UserCustomProfile.objects.filter(curp=curp).exists():
            return JsonResponse({
                'success': False,
                'field_errors': {
                    'curp': 'Este CURP ya está registrado en el sistema.'
                }
            }, status=400)
        
        # Call the parent registration method
        response = super().post(request)
        
        # If registration was successful, save custom fields
        if response.status_code == 200:
            try:
                # Get the created user
                email = request.POST.get('email')
                user = User.objects.get(email=email)
                
                # Save custom registration data
                save_custom_registration_data(user, custom_fields)
                
                logger.info(f"Custom profile created successfully for user: {user.username}")
                
            except User.DoesNotExist:
                logger.error(f"User not found after registration: {email}")
            except ValidationError as e:
                logger.error(f"Validation error saving custom profile: {e}")
                # Return validation errors to frontend
                return JsonResponse({
                    'success': False,
                    'field_errors': e.message_dict if hasattr(e, 'message_dict') else {'general': str(e)}
                }, status=400)
            except Exception as e:
                logger.error(f"Error saving custom profile: {e}")
                # Don't fail the registration, but log the error
                pass
        
        return response


@method_decorator(csrf_exempt, name='dispatch')
class ValidateCustomFieldView(APIView):
    """
    API view to validate individual custom fields
    """
    
    @require_http_methods(["POST"])
    def post(self, request):
        """
        Validate individual custom fields
        """
        try:
            data = json.loads(request.body)
            field_name = data.get('field_name')
            field_value = data.get('field_value')
            
            errors = {}
            
            if field_name == 'curp':
                if UserCustomProfile.objects.filter(curp=field_value.upper()).exists():
                    errors['curp'] = 'Este CURP ya está registrado.'
            
            # Add more field validations as needed
            
            return JsonResponse({
                'valid': len(errors) == 0,
                'errors': errors
            })
            
        except Exception as e:
            logger.error(f"Error validating custom field: {e}")
            return JsonResponse({
                'valid': False,
                'errors': {'general': 'Error de validación'}
            }, status=500)
