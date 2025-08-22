"""
Middleware para capturar y procesar datos de registro personalizado
"""
import json
import logging
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

class CustomRegistrationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """Capturar datos custom del request de registro"""
        
        # Solo procesar requests de registro
        if request.path.startswith('/api/user/v1/account/registration/') and request.method == 'POST':
            logger.info(f"Processing registration request from {request.META.get('REMOTE_ADDR')}")
            
            try:
                # Obtener datos del body
                if hasattr(request, 'body'):
                    body_data = json.loads(request.body.decode('utf-8'))
                    logger.info(f"Registration data received: {list(body_data.keys())}")
                    
                    # Campos mexicanos que buscamos
                    mexican_fields = [
                        'primer_apellido', 'segundo_apellido', 'numero_telefono',
                        'estado', 'municipio', 'nombre_escuela', 'cct', 'grado', 'curp'
                    ]
                    
                    # Extraer datos custom
                    custom_data = {}
                    for field in mexican_fields:
                        if field in body_data and body_data[field]:
                            custom_data[field] = body_data[field]
                    
                    if custom_data:
                        logger.info(f"Custom Mexican data found: {custom_data}")
                        # Guardar en el request para uso posterior
                        request.custom_registration_data = custom_data
                        
                        # TEMPORAL: Modificar first_name y last_name en el request
                        if 'primer_apellido' in custom_data:
                            body_data['name'] = custom_data['primer_apellido']
                            if 'segundo_apellido' in custom_data:
                                body_data['name'] += f" {custom_data['segundo_apellido']}"
                        
                        # Actualizar el body del request
                        request._body = json.dumps(body_data).encode('utf-8')
                        
                    else:
                        logger.warning("No custom Mexican data found in registration request")
                        
            except Exception as e:
                logger.error(f"Error processing registration request: {e}")
        
        return None
    
    def process_response(self, request, response):
        """Procesar respuesta después del registro"""
        
        if (hasattr(request, 'custom_registration_data') and 
            request.path.startswith('/api/user/v1/account/registration/') and 
            response.status_code == 200):
            
            try:
                # Buscar el usuario recién creado
                if hasattr(request, 'user') and request.user.is_authenticated:
                    user = request.user
                elif 'username' in request.custom_registration_data:
                    try:
                        user = User.objects.get(username=request.custom_registration_data['username'])
                    except User.DoesNotExist:
                        # Buscar por email si no funciona username
                        response_data = json.loads(response.content.decode('utf-8'))
                        if 'email' in response_data:
                            user = User.objects.get(email=response_data['email'])
                        else:
                            user = None
                else:
                    user = None
                
                if user:
                    logger.info(f"Found user {user.username}, saving custom data to auth_userprofile")
                    
                    custom_data = request.custom_registration_data
                    
                    # 1. Guardar en campos básicos de User
                    if 'primer_apellido' in custom_data:
                        user.first_name = custom_data['primer_apellido']
                    if 'segundo_apellido' in custom_data:
                        user.last_name = custom_data['segundo_apellido']
                    
                    user.save()
                    logger.info(f"Saved basic user data for {user.username}")
                    
                    # 2. Guardar en auth_userprofile
                    try:
                        from django.db import connection
                        cursor = connection.cursor()
                        
                        # Preparar datos para auth_userprofile
                        profile_data = {
                            'name': f"{custom_data.get('primer_apellido', '')} {custom_data.get('segundo_apellido', '')}".strip(),
                            'phone_number': custom_data.get('numero_telefono', ''),
                            'state': custom_data.get('estado', '')[:2],  # Máximo 2 caracteres
                            'city': custom_data.get('municipio', ''),
                            'meta': json.dumps({
                                'primer_apellido': custom_data.get('primer_apellido', ''),
                                'segundo_apellido': custom_data.get('segundo_apellido', ''),
                                'numero_telefono': custom_data.get('numero_telefono', ''),
                                'estado': custom_data.get('estado', ''),
                                'municipio': custom_data.get('municipio', ''),
                                'nombre_escuela': custom_data.get('nombre_escuela', ''),
                                'cct': custom_data.get('cct', ''),
                                'grado': custom_data.get('grado', ''),
                                'curp': custom_data.get('curp', '')
                            })
                        }
                        
                        # Insertar o actualizar auth_userprofile
                        cursor.execute("""
                        INSERT INTO auth_userprofile 
                        (user_id, name, phone_number, state, city, meta, courseware, language, location) 
                        VALUES (%s, %s, %s, %s, %s, %s, '', '', '')
                        ON DUPLICATE KEY UPDATE 
                        name = VALUES(name),
                        phone_number = VALUES(phone_number),
                        state = VALUES(state),
                        city = VALUES(city),
                        meta = VALUES(meta)
                        """, [
                            user.id,
                            profile_data['name'],
                            profile_data['phone_number'],
                            profile_data['state'],
                            profile_data['city'],
                            profile_data['meta']
                        ])
                        
                        logger.info(f"Successfully saved custom data to auth_userprofile for {user.username}")
                        logger.info(f"Profile data: {profile_data}")
                        
                    except Exception as e:
                        logger.error(f"Error saving to auth_userprofile: {e}")
                        # Fallback: al menos guardar en user
                        logger.info("Fallback: data saved only in auth_user fields")
                
            except Exception as e:
                logger.error(f"Error saving custom registration data: {e}")
        
        return response
