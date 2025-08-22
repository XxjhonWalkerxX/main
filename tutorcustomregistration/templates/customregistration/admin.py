"""
Django admin configuration for custom registration fields
"""
from django.contrib import admin
from .models import UserCustomProfile


@admin.register(UserCustomProfile)
class UserCustomProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserCustomProfile
    """
    list_display = [
        'user', 'primer_apellido', 'segundo_apellido', 
        'estado', 'municipio', 'nombre_escuela', 'curp', 
        'created_at'
    ]
    list_filter = ['estado', 'municipio', 'grado', 'created_at']
    search_fields = [
        'user__username', 'user__email', 'primer_apellido', 
        'segundo_apellido', 'curp', 'nombre_escuela', 'cct'
    ]
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Información Personal', {
            'fields': ('primer_apellido', 'segundo_apellido', 'numero_telefono', 'curp')
        }),
        ('Ubicación', {
            'fields': ('estado', 'municipio')
        }),
        ('Información Educativa', {
            'fields': ('nombre_escuela', 'cct', 'grado')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        # Make user field readonly when editing existing objects
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields
