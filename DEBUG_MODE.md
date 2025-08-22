# Middleware de Debug - Solo Logging

Si sigues teniendo problemas, puedes usar esta versión que **NO valida nada** y solo hace logging:

```python
# En middleware.py - Reemplazar _validate_custom_fields con:

def _validate_custom_fields(self, data):
    """DEBUG MODE - Solo logging, sin validación"""
    logger.info(f"🔍 DEBUG - Datos recibidos: {data}")
    
    # Analizar cada campo
    for field, value in data.items():
        logger.info(f"  {field}: '{value}' (tipo: {type(value)}, len: {len(str(value))})")
    
    # NO VALIDAR NADA - Solo logging
    return {}  # Sin errores
```

**Para usar modo debug:**

1. Reemplaza la función `_validate_custom_fields` con la versión de arriba
2. Reinstala el plugin
3. Prueba registro
4. Ve los logs para entender qué datos llegan

**Comandos:**
```bash
sudo tutor local stop
sudo cp -r /home/azureuser/registro-plugins /opt/
sudo tutor plugins uninstall customregistration
sudo tutor plugins install /opt/registro-plugins  
sudo tutor images build openedx
sudo tutor local start -d

# Ver logs en tiempo real
sudo tutor local logs lms | grep -E "(🔍|💾|✅|❌|💥)"
```
