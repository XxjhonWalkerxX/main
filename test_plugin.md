# Prueba del Plugin Modificado

## Pasos para probar en Azure MV:

1. **Detener Tutor:**
```bash
sudo tutor local stop
```

2. **Copiar plugin modificado:**
```bash
sudo cp -r /home/azureuser/registro-plugins /opt/
sudo chown -R root:root /opt/registro-plugins
```

3. **Reinstalar el plugin:**
```bash
sudo tutor plugins uninstall customregistration
sudo tutor plugins install /opt/registro-plugins
```

4. **Verificar instalación:**
```bash
sudo tutor plugins list
```

5. **Rebuilder y arrancar:**
```bash
sudo tutor images build openedx
sudo tutor local start -d
```

6. **Verificar logs:**
```bash
sudo tutor local logs lms
```

## Qué esperar:

Con las modificaciones actuales:
- ✅ No debería haber errores de importación de módulos Django
- ✅ Los campos personalizados seguirán estando disponibles para el frontend
- ❌ La validación backend no funcionará (temporalmente comentada)
- ❌ Los datos adicionales no se guardarán en base de datos (temporalmente deshabilitado)

## Siguiente paso si funciona:

Si no hay errores de Django, podemos implementar una aproximación diferente para la validación y guardado usando signals o middleware personalizado.
