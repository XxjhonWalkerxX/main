import json
import logging
from datetime import datetime
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)
User = get_user_model()

def save_mexican_registration_data(user_id, mexican_data):
    """Guarda los datos mexicanos en auth_userprofile.meta"""
    try:
        from student.models import UserProfile
        from django.contrib.auth import get_user_model
        
        User = get_user_model()
        user = User.objects.get(id=user_id)
        
        # Obtener o crear perfil
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'name': f"{user.first_name} {user.last_name}".strip() or user.username
            }
        )
        
        # Preparar meta data
        meta_info = {
            'mexican_registration_data': mexican_data,
            'registration_timestamp': datetime.now().isoformat(),
            'data_source': 'registration_form_processed'
        }
        
        # Combinar con meta existente si lo hay
        if profile.meta:
            try:
                existing = json.loads(profile.meta) if isinstance(profile.meta, str) else profile.meta
                existing.update(meta_info)
                profile.meta = json.dumps(existing)
            except:
                profile.meta = json.dumps(meta_info)
        else:
            profile.meta = json.dumps(meta_info)
            
        profile.save()
        logger.info(f"✅ Datos mexicanos guardados para user_id: {user_id}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error guardando datos mexicanos para user_id {user_id}: {e}")
        return False

@receiver(post_save, sender=User)
def process_new_user(sender, instance, created, **kwargs):
    """Procesa usuarios recién creados para capturar datos mexicanos"""
    if not created:
        return  # Solo procesar usuarios nuevos
        
    try:
        # Por ahora, crear perfil básico para que sepamos que el usuario fue procesado
        # Los datos reales se capturarán cuando mejoremos el sistema
        basic_mexican_data = {
            'primer_apellido': instance.first_name or '',
            'segundo_apellido': instance.last_name or '',
            'numero_telefono': '',
            'estado': '',
            'municipio': '',
            'nombre_escuela': '',
            'cct': '',
            'grado': '',
            'curp': '',
            'processed_basic': True
        }
        
        # Guardamos los datos básicos
        save_mexican_registration_data(instance.id, basic_mexican_data)
        
    except Exception as e:
        logger.error(f"❌ Error procesando nuevo usuario {instance.username}: {e}")

# Intentar conectar a más señales específicas de Open edX
try:
    from openedx.core.djangoapps.user_api.accounts.signals import USER_ACCOUNT_ACTIVATED
    
    @receiver(USER_ACCOUNT_ACTIVATED)
    def process_activated_user(sender, **kwargs):
        """Procesa cuando se activa una cuenta"""
        user = kwargs.get('user')
        if user:
            logger.info(f"📧 Usuario activado: {user.username}")
            # Aquí podríamos hacer procesamiento adicional si es necesario
            
except ImportError:
    logger.warning("⚠️  USER_ACCOUNT_ACTIVATED no disponible")

try:
    from student.signals import ACCOUNT_CREATED
    
    @receiver(ACCOUNT_CREATED)
    def process_account_created(sender, **kwargs):
        """Procesa cuando se crea una cuenta"""
        user = kwargs.get('user')
        if user:
            logger.info(f"🆕 Cuenta creada: {user.username}")
            
except ImportError:
    logger.warning("⚠️  ACCOUNT_CREATED no disponible")
