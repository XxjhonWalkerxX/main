#!/usr/bin/env python3
"""
Script para consultar los datos personalizados guardados en perfiles de usuario
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.envs.production')
django.setup()

from django.contrib.auth import get_user_model
from student.models import UserProfile

User = get_user_model()

def query_custom_profiles():
    """Consulta usuarios con datos personalizados"""
    print("🔍 Consultando usuarios con datos mexicanos personalizados...\n")
    
    profiles = UserProfile.objects.filter(meta__isnull=False).exclude(meta__exact={})
    
    for profile in profiles:
        user = profile.user
        meta = profile.meta or {}
        
        # Buscar campos mexicanos
        mexican_fields = ['primer_apellido', 'segundo_apellido', 'numero_telefono', 
                         'estado', 'municipio', 'nombre_escuela', 'cct', 'grado', 'curp']
        
        custom_data = {field: meta.get(field) for field in mexican_fields if field in meta}
        
        if custom_data:
            print(f"👤 Usuario: {user.username} ({user.email})")
            print(f"   Registrado: {user.date_joined}")
            for field, value in custom_data.items():
                print(f"   {field}: {value}")
            print()

if __name__ == "__main__":
    query_custom_profiles()
