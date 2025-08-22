"""
Custom middleware for handling registration with extended fields
"""
import json
import logging
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class CustomRegistrationMiddleware(MiddlewareMixin):
    """
    Middleware to handle custom registration fields processing
    """
    
    def process_request(self, request):
        """
        Process incoming registration requests
        """
        # Only process POST requests to registration endpoints
        if (request.method == 'POST' and 
            request.path in ['/api/user/v1/account/registration/', '/register']):
            
            # Log the custom fields for debugging
            custom_fields = [
                'primer_apellido', 'segundo_apellido', 'numero_telefono',
                'estado', 'municipio', 'nombre_escuela', 'cct', 'grado', 'curp'
            ]
            
            found_fields = []
            for field in custom_fields:
                if field in request.POST:
                    found_fields.append(field)
            
            if found_fields:
                logger.info(f"Custom registration fields detected: {found_fields}")
        
        return None
    
    def process_response(self, request, response):
        """
        Process registration responses
        """
        return response
