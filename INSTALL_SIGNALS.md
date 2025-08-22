# Plugin con Validación usando Django Signals

## ✅ **Estado actual:**
- ✅ Servidor funcionando sin errores
- ✅ Campos definidos en `REGISTRATION_EXTRA_FIELDS`
- ✅ Frontend MFE enviando datos correctamente

## 🚀 **Nueva implementación - Signals y Validación:**

### **Qué agregamos:**
1. **Django Signals** - Para procesar usuarios nuevos
2. **Validación personalizada** - Campos mexicanos (CURP, CCT, teléfono)
3. **Script de procesamiento** - Para datos de registros existentes

### **Archivos nuevos:**
- `tutorcustomregistration/signals.py` - Validación y guardado
- `process_custom_registration.py` - Script para procesar datos manualmente

## 📦 **Instalación de la nueva versión:**

```bash
# 1. Parar Tutor
sudo tutor local stop

# 2. Actualizar plugin
sudo cp -r /home/azureuser/registro-plugins /opt/
sudo chown -R root:root /opt/registro-plugins

# 3. Reinstalar plugin
sudo tutor plugins uninstall customregistration
sudo tutor plugins install /opt/registro-plugins

# 4. Verificar
sudo tutor plugins list

# 5. Rebuild e iniciar
sudo tutor images build openedx
sudo tutor local start -d
```

## 🧪 **Probar validación personalizada:**

```bash
# 1. Probar registro desde tu MFE con datos inválidos:
#    - CURP muy corto: "GALO123"  
#    - CCT muy corto: "09D"
#    - Teléfono muy corto: "555"

# 2. Ver logs de validación
sudo tutor local logs lms | grep -E "(CURP|CCT|teléfono)"

# 3. Procesar datos de usuarios recientes
sudo tutor local exec lms python /opt/registro-plugins/process_custom_registration.py

# 4. Consultar usuarios con datos personalizados
sudo tutor local exec lms python /opt/registro-plugins/query_profiles.py
```

## 🎯 **Qué debería pasar:**

### **Con datos válidos:**
- ✅ Registro exitoso 
- ✅ Datos guardados en profile.meta
- ✅ Logs: "✅ Custom fields validated successfully"

### **Con datos inválidos:**
- ❌ Error 400 con mensajes específicos
- ❌ Logs: "❌ Custom field validation errors"

### **Campos que se validan:**
- **CURP:** Entre 15-20 caracteres (más permisivo)
- **CCT:** Entre 8-12 caracteres (más permisivo)
- **Teléfono:** Entre 8-12 dígitos (más permisivo)

## 🔍 **Debug y logs:**

```bash
# Ver todos los logs
sudo tutor local logs lms | tail -100

# Ver solo validación personalizada
sudo tutor local logs lms | grep -E "(🔍|✅|❌|CURP|CCT)"

# Ver registros en tiempo real
sudo tutor local logs lms -f | grep registration
```

## 💾 **Consultar datos guardados:**

```bash
# Script para ver usuarios con datos mexicanos
sudo tutor local exec lms python /opt/registro-plugins/query_profiles.py

# Ver directamente en base de datos
sudo tutor local exec lms python manage.py shell << 'EOF'
from student.models import UserProfile
profiles = UserProfile.objects.filter(meta__isnull=False)
for p in profiles[:5]:
    if p.meta and any(field in p.meta for field in ['curp', 'cct', 'primer_apellido']):
        print(f"User: {p.user.username}, Meta: {p.meta}")
EOF
```

¡Prueba el registro con esta nueva versión y comparte los logs!
