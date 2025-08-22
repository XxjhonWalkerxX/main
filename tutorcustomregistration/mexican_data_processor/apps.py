from django.apps import AppConfig
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MexicanDataProcessorConfig(AppConfig):
    name = 'tutorcustomregistration.mexican_data_processor'
    label = 'mexican_data_processor'
    verbose_name = 'Mexican Registration Data Processor'
    
    def ready(self):
        """Se ejecuta cuando Django ha cargado completamente"""
        # Solo conectar señales si estamos en LMS y no en migraciones
        if hasattr(settings, 'SERVICE_VARIANT') and settings.SERVICE_VARIANT == 'lms':
            try:
                from . import signals
                logger.info("✅ Señales mexicanas conectadas correctamente")
            except Exception as e:
                logger.error(f"❌ Error conectando señales mexicanas: {e}")
        else:
            logger.info("⏭️  No es LMS, omitiendo señales mexicanas")
