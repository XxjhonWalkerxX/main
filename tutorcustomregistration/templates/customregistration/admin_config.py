"""
Django admin configuration for custom registration fields
"""
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserCustomProfile


class UserCustomProfileInline(admin.StackedInline):
    """
    Inline admin for custom profile fields
    """
    model = UserCustomProfile
    can_delete = False
    verbose_name_plural = 'Información Personal Mexicana'
    fields = (
        ('primer_apellido', 'segundo_apellido'),
        'numero_telefono',
        ('estado', 'municipio'),
        'nombre_escuela',
        ('cct', 'grado'),
        'curp',
    )
    readonly_fields = ('created_at', 'updated_at')


class UserCustomProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserCustomProfile
    """
    list_display = (
        'user', 
        'primer_apellido', 
        'segundo_apellido', 
        'estado', 
        'municipio',
        'nombre_escuela',
        'grado',
        'curp',
        'created_at'
    )
    
    list_filter = (
        'estado',
        'grado',
        'created_at',
        'updated_at'
    )
    
    search_fields = (
        'user__username',
        'user__email', 
        'user__first_name',
        'primer_apellido',
        'segundo_apellido',
        'curp',
        'nombre_escuela',
        'cct',
        'municipio'
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Usuario', {
            'fields': ('user',)
        }),
        ('Información Personal', {
            'fields': (
                ('primer_apellido', 'segundo_apellido'),
                'numero_telefono',
                'curp'
            )
        }),
        ('Ubicación', {
            'fields': (
                ('estado', 'municipio'),
            )
        }),
        ('Información Educativa', {
            'fields': (
                'nombre_escuela',
                ('cct', 'grado'),
            )
        }),
        ('Metadatos', {
            'fields': (
                ('created_at', 'updated_at'),
            ),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related
        """
        return super().get_queryset(request).select_related('user')


class CustomUserAdmin(BaseUserAdmin):
    """
    Extended User admin with custom profile inline
    """
    inlines = (UserCustomProfileInline,)
    
    def get_inline_instances(self, request, obj=None):
        """
        Only show inline for existing users
        """
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


# Register the models
admin.site.register(UserCustomProfile, UserCustomProfileAdmin)

# Extend the existing User admin
try:
    admin.site.unregister(User)
    admin.site.register(User, CustomUserAdmin)
except admin.sites.AlreadyRegistered:
    # If User is already registered with custom admin, skip
    pass
