# INSTALACIÓN SUPER RÁPIDA - CAMPOS MUY PERMISIVOS

## 🚨 **NUEVA VERSIÓN - TODO OPCIONAL EXCEPTO PRIMER_APELLIDO**

### **Cambios aplicados:**
- ✅ Solo `primer_apellido` es obligatorio
- ✅ Todos los demás campos son opcionales
- ✅ Sin regex restrictivos
- ✅ Rangos muy amplios

### **Validación con tus datos del log:**
```json
"cct": ["12133454345"],           // ✅ 11 caracteres - VÁLIDO (rango: 3-30)
"curp": ["123456789123456789"],   // ✅ 18 caracteres - VÁLIDO (rango: 5-30) 
"numero_telefono": ["5611623076"], // ✅ 10 dígitos - VÁLIDO (rango: 5-20)
"primer_apellido": ["Pariatu"]    // ✅ 7 caracteres - VÁLIDO (obligatorio)
```

## ⚡ **INSTALACIÓN INMEDIATA:**

```bash
# Una sola línea - TODO EN UNO
sudo tutor local stop && sudo cp -r /home/azureuser/registro-plugins /opt/ && sudo chown -R root:root /opt/registro-plugins && sudo tutor plugins uninstall customregistration && sudo tutor plugins install /opt/registro-plugins && sudo tutor plugins enable customregistration && sudo tutor images build openedx && sudo tutor local start -d

# Ver logs en tiempo real
sudo tutor local logs lms -f | grep registration
```

## 📊 **Qué debería pasar AHORA:**

### ✅ **Con los datos de tu último log:**
- `primer_apellido: "Pariatu"` ← VÁLIDO (obligatorio)
- `cct: "12133454345"` ← VÁLIDO (11 chars, rango 3-30)
- `curp: "123456789123456789"` ← VÁLIDO (18 chars, rango 5-30)
- `numero_telefono: "5611623076"` ← VÁLIDO (10 chars, rango 5-20)

### 🎯 **Resultado esperado:**
- ✅ HTTP 200 (éxito)
- ✅ Usuario `qeqomeles` creado
- ✅ Email `dakatuguqo@mailinator.com` registrado

Si AÚN falla después de esto, entonces hay otro problema más profundo en Open edX que no está relacionado con nuestros campos personalizados.

## 🔍 **Para verificar éxito:**

```bash
# Después del registro exitoso, consultar usuario
sudo tutor local exec lms python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.filter(username='qeqomeles').first()
if user:
    print(f"✅ Usuario creado: {user.username} - {user.email}")
    from student.models import UserProfile
    profile = UserProfile.objects.filter(user=user).first()
    if profile and profile.meta:
        print(f"✅ Datos guardados: {profile.meta}")
    else:
        print("❌ Sin datos personalizados")
else:
    print("❌ Usuario no encontrado")
EOF
```

**¡EJECUTA LA INSTALACIÓN Y PRUEBA INMEDIATAMENTE!**
