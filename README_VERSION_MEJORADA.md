# Plugin de Registro Mexicano - Versión Mejorada

## ✅ Lo que SÍ funciona de forma segura:

1. **Campos de registro mexicanos** - Definidos y funcionando
2. **Registro sin problemas** - Los usuarios se pueden registrar
3. **App Django separada** - Manejo seguro de señales sin romper LMS

## 🚧 Lo que está en desarrollo:

1. **Captura de datos del formulario** - Actualmente captura datos básicos (nombre/apellido)
2. **Datos completos mexicanos** - Necesita mejorar la captura desde el request POST

## 📁 Estructura del Plugin:

```
tutorcustomregistration/
├── __init__.py
├── plugin.py                          # Configuración principal y campos
├── mexican_data_processor/             # App Django para capturar datos
│   ├── __init__.py
│   ├── apps.py                        # Configuración de la app
│   └── signals.py                     # Señales para capturar datos
```

## 🎯 Cómo funciona:

1. **Plugin principal**: Define los 9 campos mexicanos en el formulario
2. **App separada**: Se ejecuta después del registro para capturar y guardar datos
3. **Señales Django**: Conecta automáticamente cuando se crea un usuario
4. **Meta storage**: Guarda datos en `auth_userprofile.meta` como JSON

## 🔧 Instalación:

```bash
# En tu servidor Azure:
tutor plugins disable customregistration
tutor plugins install ./tutorcustomregistration  
tutor plugins enable customregistration
tutor local rebuild openedx
tutor local restart
```

## 📊 Verificar datos:

```sql
SELECT u.username, up.meta 
FROM auth_user u 
JOIN auth_userprofile up ON u.id = up.user_id 
WHERE up.meta IS NOT NULL 
ORDER BY u.date_joined DESC 
LIMIT 5;
```

**Ventajas de esta versión:**
- ✅ No rompe el LMS durante startup
- ✅ Manejo seguro de errores
- ✅ Logging detallado para debug
- ✅ Estructura modular y mantenible
