# Plugin de Registro Personalizado - Versión con Middleware

## ✅ Estado Actual según tus logs:

**Frontend MFE:** ✅ Funcionando perfectamente
- Envía todos los campos mexicanos: `cct`, `curp`, `estado`, `municipio`, etc.
- No hay errores de CORS críticos

**Backend Plugin:** ✅ Sin errores de importación
- Plugin cargado correctamente
- Campos definidos en `REGISTRATION_EXTRA_FIELDS`

**Problema:** ❌ Backend devuelve HTTP 400 (Bad Request)
- Los campos se reciben pero no se procesan

## 🚀 Solución Implementada:

He creado un **middleware simplificado** que:
1. ✅ Intercepta requests de registro
2. ✅ Valida campos mexicanos (CURP, CCT, teléfono)  
3. ✅ No requiere apps Django adicionales
4. ✅ Devuelve errores específicos de validación

## 📦 Pasos para instalar la nueva versión:

```bash
# 1. Detener Tutor
sudo tutor local stop

# 2. Copiar plugin actualizado
sudo cp -r /home/azureuser/registro-plugins /opt/
sudo chown -R root:root /opt/registro-plugins

# 3. Reinstalar plugin
sudo tutor plugins uninstall customregistration
sudo tutor plugins install /opt/registro-plugins

# 4. Verificar instalación
sudo tutor plugins list

# 5. Rebuild (importante para instalar middleware)
sudo tutor images build openedx

# 6. Iniciar
sudo tutor local start -d

# 7. Probar registro desde tu MFE
```

## 🧪 Qué esperar:

1. **Casos válidos:** Registro exitoso con validación
2. **CURP inválido:** Error específico de formato
3. **CCT inválido:** Error específico de formato  
4. **Campos faltantes:** Errores por campo requerido

## 🔍 Para debuggear:

```bash
# Ver logs de procesamiento
sudo tutor local logs lms | grep -i "custom\|registration"

# Ver requests completos  
sudo tutor local logs lms | tail -f
```

Prueba esta versión y comparte los nuevos logs!
