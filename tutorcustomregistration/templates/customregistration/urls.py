"""
URL configuration for custom registration
"""
from django.urls import path
from .views import CustomRegistrationView, ValidateCustomFieldView

app_name = 'customregistration'

urlpatterns = [
    path('register/', CustomRegistrationView.as_view(), name='custom_register'),
    path('validate_field/', ValidateCustomFieldView.as_view(), name='validate_field'),
]
