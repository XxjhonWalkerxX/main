#!/usr/bin/env python3
"""
Script para procesar registros con campos personalizados mexicanos
Ejecutar manualmente después de registros para procesar datos adicionales
"""
import os
import sys
import django
import json
import logging
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.envs.production')
django.setup()

from django.contrib.auth import get_user_model
from student.models import UserProfile
from tutorcustomregistration.signals import CustomRegistrationHandler

User = get_user_model()
logger = logging.getLogger(__name__)

def find_recent_users(minutes=10):
    """Find users created in the last N minutes"""
    time_threshold = datetime.now() - timedelta(minutes=minutes)
    recent_users = User.objects.filter(date_joined__gte=time_threshold)
    return recent_users

def process_registration_logs():
    """Process registration logs to extract custom data"""
    # This would parse logs from /edx/var/log/lms/edx.log
    # For now, we'll simulate the process
    print("🔍 Checking for recent registrations with custom fields...")
    
    recent_users = find_recent_users(60)  # Last hour
    
    for user in recent_users:
        print(f"\n👤 User: {user.username} ({user.email})")
        print(f"   Created: {user.date_joined}")
        
        # Check if user already has custom profile data
        try:
            profile = UserProfile.objects.get(user=user)
            meta = profile.meta or {}
            
            custom_fields = ['primer_apellido', 'segundo_apellido', 'numero_telefono', 
                           'estado', 'municipio', 'nombre_escuela', 'cct', 'grado', 'curp']
            
            has_custom_data = any(field in meta for field in custom_fields)
            
            if has_custom_data:
                print("   ✅ Already has custom profile data")
                for field in custom_fields:
                    if field in meta:
                        print(f"      {field}: {meta[field]}")
            else:
                print("   ❌ No custom profile data found")
                
        except UserProfile.DoesNotExist:
            print("   ❓ No profile found")

def simulate_custom_data_processing(username, custom_data):
    """Simulate processing custom registration data for a user"""
    try:
        user = User.objects.get(username=username)
        
        # Validate data
        errors = CustomRegistrationHandler.validate_mexican_fields(custom_data)
        
        if errors:
            print(f"❌ Validation errors for {username}: {errors}")
            return False
        
        # Save data
        success = CustomRegistrationHandler.save_custom_profile_data(user, custom_data)
        
        if success:
            print(f"✅ Successfully processed custom data for {username}")
            return True
        else:
            print(f"❌ Failed to save custom data for {username}")
            return False
            
    except User.DoesNotExist:
        print(f"❌ User {username} not found")
        return False

def main():
    print("🚀 Custom Registration Data Processor")
    print("=" * 50)
    
    # Process recent registrations
    process_registration_logs()
    
    print("\n" + "=" * 50)
    print("💡 To process custom data for a specific user:")
    print("   python process_custom_registration.py --user USERNAME")
    print("\n💡 To test with sample data:")
    print("   python process_custom_registration.py --test")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == '--test':
            # Test with sample data
            sample_data = {
                'primer_apellido': 'García',
                'segundo_apellido': 'López',
                'numero_telefono': '5551234567',
                'estado': 'CDMX',
                'municipio': 'Coyoacán',
                'nombre_escuela': 'Escuela Primaria Benito Juárez',
                'cct': '09DPR1234K',
                'grado': '6to Grado',
                'curp': 'GALO801201HDFRNL05'
            }
            
            recent_users = find_recent_users(60)
            if recent_users:
                test_user = recent_users[0]
                print(f"\n🧪 Testing with user: {test_user.username}")
                simulate_custom_data_processing(test_user.username, sample_data)
            else:
                print("\n❌ No recent users found for testing")
                
        elif sys.argv[1] == '--user' and len(sys.argv) > 2:
            username = sys.argv[2]
            print(f"\n🔍 Processing user: {username}")
            # Here you would extract the actual custom data from logs or other source
            print("   💡 Custom data would need to be extracted from registration logs")
            
    else:
        main()
