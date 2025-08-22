"""
Custom registration forms for extended fields
"""
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from openedx.core.djangoapps.user_authn.forms import RegistrationFormFactory

from .models import UserCustomProfile, validate_curp, validate_cct, validate_phone


class CustomRegistrationExtensionForm(forms.Form):
    """
    Extension form for custom registration fields
    This form handles the additional fields for Mexican users
    """
    
    primer_apellido = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu primer apellido'
        }),
        error_messages={
            'required': 'El primer apellido es obligatorio.',
            'max_length': 'El primer apellido no puede tener más de 100 caracteres.'
        }
    )
    
    segundo_apellido = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu segundo apellido (opcional)'
        }),
        error_messages={
            'max_length': 'El segundo apellido no puede tener más de 100 caracteres.'
        }
    )
    
    numero_telefono = forms.CharField(
        max_length=10,
        min_length=10,
        required=True,
        validators=[validate_phone],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '1234567890',
            'maxlength': '10',
            'pattern': '[0-9]{10}'
        }),
        error_messages={
            'required': 'El número de teléfono es obligatorio.',
            'invalid': 'El teléfono debe tener exactamente 10 dígitos.',
            'min_length': 'El teléfono debe tener 10 dígitos.',
            'max_length': 'El teléfono debe tener 10 dígitos.'
        }
    )
    
    estado = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Estado de residencia'
        }),
        error_messages={
            'required': 'El estado es obligatorio.',
            'max_length': 'El estado no puede tener más de 100 caracteres.'
        }
    )
    
    municipio = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Municipio de residencia'
        }),
        error_messages={
            'required': 'El municipio es obligatorio.',
            'max_length': 'El municipio no puede tener más de 100 caracteres.'
        }
    )
    
    nombre_escuela = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre completo de tu escuela'
        }),
        error_messages={
            'required': 'El nombre de la escuela es obligatorio.',
            'max_length': 'El nombre de la escuela no puede tener más de 200 caracteres.'
        }
    )
    
    cct = forms.CharField(
        max_length=10,
        min_length=10,
        required=True,
        validators=[validate_cct],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12ABC3456D',
            'maxlength': '10',
            'style': 'text-transform: uppercase;'
        }),
        error_messages={
            'required': 'La CCT es obligatoria.',
            'invalid': 'La CCT debe tener el formato válido (10 caracteres).',
            'min_length': 'La CCT debe tener 10 caracteres.',
            'max_length': 'La CCT debe tener 10 caracteres.'
        }
    )
    
    grado = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ej: 1° de Secundaria'
        }),
        error_messages={
            'required': 'El grado es obligatorio.',
            'max_length': 'El grado no puede tener más de 50 caracteres.'
        }
    )
    
    curp = forms.CharField(
        max_length=18,
        min_length=18,
        required=True,
        validators=[validate_curp],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ABCD123456HEFGHI01',
            'maxlength': '18',
            'style': 'text-transform: uppercase;'
        }),
        error_messages={
            'required': 'El CURP es obligatorio.',
            'invalid': 'El CURP debe tener el formato válido mexicano.',
            'min_length': 'El CURP debe tener 18 caracteres.',
            'max_length': 'El CURP debe tener 18 caracteres.'
        }
    )
    
    def clean_curp(self):
        """
        Validate that CURP is unique
        """
        curp = self.cleaned_data.get('curp', '').upper()
        
        if UserCustomProfile.objects.filter(curp=curp).exists():
            raise ValidationError('Este CURP ya está registrado en el sistema.')
        
        return curp
    
    def clean_cct(self):
        """
        Convert CCT to uppercase
        """
        cct = self.cleaned_data.get('cct', '').upper()
        return cct
    
    def save(self, user):
        """
        Save the custom profile data for the given user
        
        Args:
            user: The User instance to associate with the profile
            
        Returns:
            UserCustomProfile: The created profile instance
        """
        profile = UserCustomProfile.objects.create(
            user=user,
            primer_apellido=self.cleaned_data['primer_apellido'],
            segundo_apellido=self.cleaned_data.get('segundo_apellido', ''),
            numero_telefono=self.cleaned_data['numero_telefono'],
            estado=self.cleaned_data['estado'],
            municipio=self.cleaned_data['municipio'],
            nombre_escuela=self.cleaned_data['nombre_escuela'],
            cct=self.cleaned_data['cct'],
            grado=self.cleaned_data['grado'],
            curp=self.cleaned_data['curp'],
        )
        
        return profile
