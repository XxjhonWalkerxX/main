# Test file to verify plugin compatibility
import sys
import pkg_resources

def check_tutor_version():
    """Check if Tutor is installed and get version"""
    try:
        tutor_version = pkg_resources.get_distribution("tutor").version
        print(f"✅ Tutor version: {tutor_version}")
        
        # Parse version
        major, minor, patch = tutor_version.split('.')
        if int(major) >= 19:
            print("✅ Tutor version is compatible (>= 19.0.0)")
            return True
        else:
            print("❌ Tutor version is too old. Need >= 19.0.0")
            return False
            
    except pkg_resources.DistributionNotFound:
        print("❌ Tutor is not installed")
        return False

def check_plugin_structure():
    """Check if plugin structure is correct"""
    import os
    
    required_files = [
        'tutorcustomregistration/plugin.py',
        'tutorcustomregistration/templates/customregistration/models.py',
        'tutorcustomregistration/templates/customregistration/views.py',
        'tutorcustomregistration/templates/customregistration/forms.py',
        'setup.py'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
            all_exist = False
    
    return all_exist

if __name__ == "__main__":
    print("🔍 Checking plugin compatibility for Tutor 19.0.0...")
    print("-" * 50)
    
    tutor_ok = check_tutor_version()
    structure_ok = check_plugin_structure()
    
    print("-" * 50)
    if tutor_ok and structure_ok:
        print("🎉 Plugin is ready for Tutor 19.0.0!")
        print("\nNext steps:")
        print("1. git add . && git commit -m 'Initial plugin version'")
        print("2. git push")
        print("3. Install on your MV following INSTALACION_MV.md")
    else:
        print("❌ Plugin has issues. Please fix them first.")
