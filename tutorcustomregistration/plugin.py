from tutor import hooks
import os
import sys
import json

# Plugin metadata
__version__ = "1.0.0"
name = "customregistration"

# Plugin configuration
config = {
    "add": [
        ("CUSTOM_REGISTRATION_ENABLED", True),
    ]
}

# Hook para procesar datos de registro personalizados
@hooks.Actions.CORE_READY.add()
def setup_custom_registration_processor():
    """Setup custom registration data processor using Tutor hooks"""
    print("✅ Custom registration processor initialized")

# Plugin patches con procesamiento de datos integrado
hooks.Filters.ENV_PATCHES.add_items([
    # LMS settings patch
    ("openedx-lms-production-settings", """
# Custom registration fields configuration
CUSTOM_REGISTRATION_FIELDS_ENABLED = True
ENABLE_DYNAMIC_REGISTRATION_FIELDS = True

# Disable terms of service requirement completely
ENABLE_REGISTRATION_TERMS_OF_SERVICE = False

# Logging para debug
LOGGING['loggers']['tutorcustomregistration'] = {
    'handlers': ['console'],
    'level': 'INFO',
    'propagate': True,
}

# Import required modules for custom registration processing
import json
import logging
from django.db import connection
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save

# Setup logger
custom_logger = logging.getLogger('tutorcustomregistration')

# Custom registration signal handler
@receiver(post_save, sender=get_user_model())
def process_custom_registration_data(sender, instance, created, **kwargs):
    '''Process custom Mexican registration data after user creation'''
    if not created:
        return  # Solo procesar usuarios nuevos
    
    try:
        custom_logger.info(f"Processing custom data for new user: {instance.username}")
        
        # Get request data from thread-local storage if available
        import threading
        current_thread = threading.current_thread()
        custom_data = getattr(current_thread, 'custom_registration_data', None)
        
        if custom_data:
            custom_logger.info(f"Found custom data: {list(custom_data.keys())}")
            
            # Save basic data to auth_user
            if 'primer_apellido' in custom_data:
                instance.first_name = custom_data['primer_apellido'][:30]  # Django limit
            if 'segundo_apellido' in custom_data:
                instance.last_name = custom_data['segundo_apellido'][:150]  # Django limit
            
            instance.save(update_fields=['first_name', 'last_name'])
            
            # Save complete data to auth_userprofile
            try:
                cursor = connection.cursor()
                
                # Prepare profile data
                profile_name = f"{custom_data.get('primer_apellido', '')} {custom_data.get('segundo_apellido', '')}".strip()
                phone_number = custom_data.get('numero_telefono', '')[:50]  # DB limit
                state = custom_data.get('estado', '')[:2]  # DB limit  
                city = custom_data.get('municipio', '')
                
                # Create complete meta JSON
                meta_json = json.dumps({
                    'primer_apellido': custom_data.get('primer_apellido', ''),
                    'segundo_apellido': custom_data.get('segundo_apellido', ''),
                    'numero_telefono': custom_data.get('numero_telefono', ''),
                    'estado': custom_data.get('estado', ''),
                    'municipio': custom_data.get('municipio', ''),
                    'nombre_escuela': custom_data.get('nombre_escuela', ''),
                    'cct': custom_data.get('cct', ''),
                    'grado': custom_data.get('grado', ''),
                    'curp': custom_data.get('curp', ''),
                    'registration_source': 'custom_mexican_fields'
                })
                
                # Insert/update auth_userprofile
                cursor.execute(\"\"\"
                INSERT INTO auth_userprofile 
                (user_id, name, phone_number, state, city, meta, courseware, language, location) 
                VALUES (%s, %s, %s, %s, %s, %s, '', '', '')
                ON DUPLICATE KEY UPDATE 
                name = VALUES(name),
                phone_number = VALUES(phone_number),
                state = VALUES(state),
                city = VALUES(city),
                meta = VALUES(meta)
                \"\"\", [
                    instance.id,
                    profile_name[:255],  # DB limit
                    phone_number,
                    state,
                    city,
                    meta_json
                ])
                
                custom_logger.info(f"✅ Successfully saved custom data to auth_userprofile for {instance.username}")
                
            except Exception as e:
                custom_logger.error(f"❌ Error saving to auth_userprofile: {e}")
                
        else:
            custom_logger.info(f"No custom data found for {instance.username}")
            
    except Exception as e:
        custom_logger.error(f"❌ Error in custom registration processor: {e}")

# Monkey patch registration view to capture custom data
def patch_registration_view():
    '''Patch the registration API to capture custom Mexican data'''
    try:
        from openedx.core.djangoapps.user_authn.views.register import RegistrationView
        original_post = RegistrationView.post
        
        def patched_post(self, request, *args, **kwargs):
            '''Patched POST method to capture custom data'''
            import threading
            
            # Extract custom Mexican fields from request
            custom_fields = ['primer_apellido', 'segundo_apellido', 'numero_telefono', 
                           'estado', 'municipio', 'nombre_escuela', 'cct', 'grado', 'curp']
            
            custom_data = {}
            for field in custom_fields:
                if field in request.data and request.data[field]:
                    custom_data[field] = str(request.data[field]).strip()
            
            if custom_data:
                # Store in thread-local for signal handler
                current_thread = threading.current_thread()
                current_thread.custom_registration_data = custom_data
                custom_logger.info(f"Captured custom Mexican data: {list(custom_data.keys())}")
            
            # Call original registration method
            return original_post(self, request, *args, **kwargs)
        
        # Apply the patch
        RegistrationView.post = patched_post
        custom_logger.info("✅ Registration view patched successfully")
        
    except Exception as e:
        custom_logger.warning(f"⚠️  Could not patch registration view: {e}")

# Apply patches when Django is ready
import django
from django.apps import apps

def apply_registration_patches():
    if apps.ready:
        patch_registration_view()
    else:
        # Wait for Django to be ready
        def on_ready():
            patch_registration_view()
        apps.app_configs_ready.connect(on_ready)

# Initialize patches
apply_registration_patches()

# Define custom registration fields - PERMISIVOS PARA FACILITAR REGISTRO
REGISTRATION_EXTRA_FIELDS = {
    'primer_apellido': {
        'type': 'text',
        'label': 'Primer Apellido',
        'required': False,
        'max_length': 100
    },
    'segundo_apellido': {
        'type': 'text', 
        'label': 'Segundo Apellido',
        'required': False,
        'max_length': 100
    },
    'numero_telefono': {
        'type': 'text',
        'label': 'Número de Teléfono', 
        'required': False,
        'max_length': 20
    },
    'estado': {
        'type': 'text',
        'label': 'Estado',
        'required': False, 
        'max_length': 100
    },
    'municipio': {
        'type': 'text',
        'label': 'Municipio',
        'required': False,
        'max_length': 100
    },
    'nombre_escuela': {
        'type': 'text',
        'label': 'Nombre de la Escuela',
        'required': False,
        'max_length': 200
    },
    'cct': {
        'type': 'text',
        'label': 'CCT',
        'required': False,
        'max_length': 30
    },
    'grado': {
        'type': 'text',
        'label': 'Grado', 
        'required': False,
        'max_length': 50
    },
    'curp': {
        'type': 'text',
        'label': 'CURP',
        'required': False,
        'max_length': 30
    }
}
"""),
])
