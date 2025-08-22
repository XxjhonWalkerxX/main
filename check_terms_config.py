#!/usr/bin/env python3
"""
Script para verificar configuraciones de términos y condiciones en Open edX
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.envs.production')
django.setup()

from django.conf import settings

def check_terms_settings():
    """Check all settings related to terms of service"""
    print("🔍 Checking Terms of Service Settings:")
    print("=" * 50)
    
    terms_settings = [
        'ENABLE_TERMS_AND_CONDITIONS_CHECKBOX',
        'REGISTRATION_EXTENSION_FORM',
        'ENABLE_REGISTRATION_TERMS_OF_SERVICE',
        'MARKETING_EMAIL_OPT_IN',
        'ENABLE_MARKETING_EMAIL_OPT_IN',
        'MARKETING_SITE_ROOT',
        'TERMS_OF_SERVICE_REQUIRED',
        'REGISTRATION_EXTRA_FIELD_SETTINGS'
    ]
    
    for setting in terms_settings:
        try:
            value = getattr(settings, setting, 'NOT_SET')
            status = "✅" if not value or value == 'NOT_SET' else "⚠️"
            print(f"{status} {setting}: {value}")
        except Exception as e:
            print(f"❓ {setting}: Error reading - {e}")
    
    print("\n🎯 Registration Fields:")
    print("=" * 30)
    
    try:
        fields = getattr(settings, 'REGISTRATION_EXTRA_FIELDS', {})
        print(f"✅ REGISTRATION_EXTRA_FIELDS: {len(fields)} fields defined")
        for field_name in fields.keys():
            print(f"   - {field_name}")
    except Exception as e:
        print(f"❌ Error reading REGISTRATION_EXTRA_FIELDS: {e}")

if __name__ == "__main__":
    check_terms_settings()
