from tutor import hooks

# Plugin metadata (required for Tutor 19.0.0)
__version__ = "1.0.0"
name = "customregistration"

# Plugin configuration
config = {
    "add": [
        ("CUSTOM_REGISTRATION_ENABLED", True),
    ]
}

# Plugin patches - usando hooks en lugar de dockerfile patches
hooks.Filters.ENV_PATCHES.add_items([
    # LMS settings patch
    ("openedx-lms-production-settings", """
# Custom registration fields configuration
CUSTOM_REGISTRATION_FIELDS_ENABLED = True

# Enable dynamic registration fields in MFE
ENABLE_DYNAMIC_REGISTRATION_FIELDS = True

# Simple middleware to process custom fields
MIDDLEWARE += ['tutor_customregistration.middleware.CustomRegistrationMiddleware']

# Add custom app to installed apps - COMENTADO TEMPORALMENTE
# INSTALLED_APPS += ['customregistration']

# Define custom registration fields that Open edX should recognize
REGISTRATION_EXTRA_FIELDS = {
    'primer_apellido': {
        'type': 'text',
        'label': 'Primer Apellido',
        'required': True,
        'max_length': 100,
        'error_messages': {
            'required': 'El primer apellido es obligatorio.',
            'max_length': 'El primer apellido no puede tener más de 100 caracteres.'
        }
    },
    'segundo_apellido': {
        'type': 'text',
        'label': 'Segundo Apellido',
        'required': False,
        'max_length': 100,
        'error_messages': {
            'max_length': 'El segundo apellido no puede tener más de 100 caracteres.'
        }
    },
    'numero_telefono': {
        'type': 'text',
        'label': 'Número de Teléfono',
        'required': True,
        'max_length': 10,
        'min_length': 10,
        'regex': r'^[0-9]{10}$',
        'error_messages': {
            'required': 'El número de teléfono es obligatorio.',
            'invalid': 'El teléfono debe tener exactamente 10 dígitos.',
            'regex': 'El teléfono debe contener solo números.'
        }
    },
    'estado': {
        'type': 'text',
        'label': 'Estado',
        'required': True,
        'max_length': 100,
        'error_messages': {
            'required': 'El estado es obligatorio.',
            'max_length': 'El estado no puede tener más de 100 caracteres.'
        }
    },
    'municipio': {
        'type': 'text',
        'label': 'Municipio',
        'required': True,
        'max_length': 100,
        'error_messages': {
            'required': 'El municipio es obligatorio.',
            'max_length': 'El municipio no puede tener más de 100 caracteres.'
        }
    },
    'nombre_escuela': {
        'type': 'text',
        'label': 'Nombre de la Escuela',
        'required': True,
        'max_length': 200,
        'error_messages': {
            'required': 'El nombre de la escuela es obligatorio.',
            'max_length': 'El nombre de la escuela no puede tener más de 200 caracteres.'
        }
    },
    'cct': {
        'type': 'text',
        'label': 'CCT',
        'required': True,
        'max_length': 10,
        'min_length': 10,
        'regex': r'^[0-9]{2}[A-Z]{3}[0-9]{4}[A-Z]$',
        'error_messages': {
            'required': 'La CCT es obligatoria.',
            'invalid': 'La CCT debe tener el formato válido (10 caracteres).',
            'regex': 'La CCT debe seguir el formato: 2 números + 3 letras + 4 números + 1 letra.'
        }
    },
    'grado': {
        'type': 'text',
        'label': 'Grado',
        'required': True,
        'max_length': 50,
        'error_messages': {
            'required': 'El grado es obligatorio.',
            'max_length': 'El grado no puede tener más de 50 caracteres.'
        }
    },
    'curp': {
        'type': 'text',
        'label': 'CURP',
        'required': True,
        'max_length': 18,
        'min_length': 18,
        'regex': r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9]{2}$',
        'error_messages': {
            'required': 'El CURP es obligatorio.',
            'invalid': 'El CURP debe tener el formato válido mexicano.',
            'regex': 'El CURP debe tener 18 caracteres en formato válido.',
            'unique': 'Este CURP ya está registrado en el sistema.'
        }
    }
}

# Extended profile fields configuration
EXTENDED_PROFILE_FIELDS = ['primer_apellido', 'segundo_apellido', 'numero_telefono', 'estado', 'municipio', 'nombre_escuela', 'cct', 'grado', 'curp']

# Registration field validation (legacy support)
REGISTRATION_FIELD_VALIDATORS = {
    'curp': {
        'regex': r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9]{2}$',
        'message': 'El CURP debe tener el formato válido mexicano'
    },
    'cct': {
        'regex': r'^[0-9]{2}[A-Z]{3}[0-9]{4}[A-Z]$',
        'message': 'La CCT debe tener el formato válido (10 caracteres)'
    },
    'numero_telefono': {
        'regex': r'^[0-9]{10}$',
        'message': 'El teléfono debe tener 10 dígitos'
    }
}
"""),

    # CMS settings patch  
    ("openedx-cms-production-settings", """
# Enable custom registration fields for Studio
CUSTOM_REGISTRATION_FIELDS_ENABLED = True
# INSTALLED_APPS += ['customregistration']  # COMENTADO TEMPORALMENTE

# Same registration fields for CMS
REGISTRATION_EXTRA_FIELDS = {
    'primer_apellido': {'type': 'text', 'label': 'Primer Apellido', 'required': True},
    'segundo_apellido': {'type': 'text', 'label': 'Segundo Apellido', 'required': False},
    'numero_telefono': {'type': 'text', 'label': 'Número de Teléfono', 'required': True},
    'estado': {'type': 'text', 'label': 'Estado', 'required': True},
    'municipio': {'type': 'text', 'label': 'Municipio', 'required': True},
    'nombre_escuela': {'type': 'text', 'label': 'Nombre de la Escuela', 'required': True},
    'cct': {'type': 'text', 'label': 'CCT', 'required': True},
    'grado': {'type': 'text', 'label': 'Grado', 'required': True},
    'curp': {'type': 'text', 'label': 'CURP', 'required': True}
}
"""),

    # Common settings for both LMS and CMS
    ("openedx-common-settings", """
# Custom registration app configuration
CUSTOM_REGISTRATION_FIELDS_ENABLED = True

# Simple backend processing without Django apps
REGISTRATION_EXTRA_FIELDS_PROCESSING = True

# Enable validation for custom fields
CUSTOM_FIELD_VALIDATION_ENABLED = True

# Simple profile field mapping
PROFILE_FIELD_MAPPING = {
    'primer_apellido': 'meta.primer_apellido',
    'segundo_apellido': 'meta.segundo_apellido', 
    'numero_telefono': 'meta.numero_telefono',
    'estado': 'meta.estado',
    'municipio': 'meta.municipio',
    'nombre_escuela': 'meta.nombre_escuela',
    'cct': 'meta.cct',
    'grado': 'meta.grado',
    'curp': 'meta.curp'
}
"""),
])

# Plugin initialization using hooks instead of dockerfile patches
@hooks.Actions.CORE_READY.add()
def _initialize_custom_registration():
    """Initialize the custom registration plugin"""
    pass

# Template files will be provided via Python package installation
# No need to modify Dockerfile
