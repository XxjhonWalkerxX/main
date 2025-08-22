"""
Models for custom registration fields
"""
import re
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_curp(value):
    """Validate Mexican CURP format"""
    curp_pattern = r'^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9]{2}$'
    if not re.match(curp_pattern, value.upper()):
        raise ValidationError('El CURP debe tener el formato válido mexicano (18 caracteres)')


def validate_cct(value):
    """Validate Mexican CCT (Clave de Centro de Trabajo) format"""
    cct_pattern = r'^[0-9]{2}[A-Z]{3}[0-9]{4}[A-Z]$'
    if not re.match(cct_pattern, value.upper()):
        raise ValidationError('La CCT debe tener el formato válido (10 caracteres)')


def validate_phone(value):
    """Validate Mexican phone number (10 digits)"""
    phone_pattern = r'^[0-9]{10}$'
    if not re.match(phone_pattern, value):
        raise ValidationError('El teléfono debe tener exactamente 10 dígitos')


class UserCustomProfile(models.Model):
    """Extended profile for Mexican users with custom fields"""
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='custom_profile'
    )
    
    # Nombres y apellidos
    primer_apellido = models.CharField(
        max_length=100, 
        verbose_name='Primer Apellido',
        help_text='Primer apellido del usuario'
    )
    segundo_apellido = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name='Segundo Apellido',
        help_text='Segundo apellido del usuario (opcional)'
    )
    
    # Información de contacto
    numero_telefono = models.CharField(
        max_length=10, 
        validators=[validate_phone],
        verbose_name='Número de Teléfono',
        help_text='Número de teléfono a 10 dígitos'
    )
    
    # Ubicación
    estado = models.CharField(
        max_length=100, 
        verbose_name='Estado',
        help_text='Estado de residencia'
    )
    municipio = models.CharField(
        max_length=100, 
        verbose_name='Municipio',
        help_text='Municipio de residencia'
    )
    
    # Información educativa
    nombre_escuela = models.CharField(
        max_length=200, 
        verbose_name='Nombre de la Escuela',
        help_text='Nombre completo de la institución educativa'
    )
    cct = models.CharField(
        max_length=10, 
        validators=[validate_cct],
        verbose_name='CCT',
        help_text='Clave de Centro de Trabajo (10 caracteres)'
    )
    grado = models.CharField(
        max_length=50, 
        verbose_name='Grado',
        help_text='Grado escolar actual'
    )
    
    # Identificación oficial
    curp = models.CharField(
        max_length=18, 
        unique=True,
        validators=[validate_curp],
        verbose_name='CURP',
        help_text='Clave Única de Registro de Población (18 caracteres)'
    )
    
    # Metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil Personalizado de Usuario'
        verbose_name_plural = 'Perfiles Personalizados de Usuarios'
        db_table = 'customregistration_usercustomprofile'
    
    def __str__(self):
        return f"{self.user.username} - {self.primer_apellido} {self.segundo_apellido}"
    
    def clean(self):
        """Additional validation"""
        # Convert CURP and CCT to uppercase
        if self.curp:
            self.curp = self.curp.upper()
        if self.cct:
            self.cct = self.cct.upper()
            
        super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
