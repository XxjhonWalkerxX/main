from tutor import hooks

# Plugin metadata
__version__ = "1.0.0"
name = "customregistration"

# Plugin configuration
config = {
    "add": [
        ("CUSTOM_REGISTRATION_ENABLED", True),
    ]
}

# Plugin patches - Solo campos, SIN captura de datos para evitar errores
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

# Crear el archivo de captura de datos por separado usando hooks
hooks.Filters.ENV_PATCHES.add_items([
    ("openedx-lms-common-settings", """
# Instalar el procesador de datos mexicanos
INSTALLED_APPS += ('tutorcustomregistration.mexican_data_processor',)
"""),
])
