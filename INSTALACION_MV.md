# Instrucciones para Instalar en MV (Azure)

## Pasos para Diego - Instalación en Servidor de Producción

### 1. Subir Plugin a Repositorio

En tu máquina local (donde tienes este código):
```bash
cd /Users/diegonicolas/Desktop/registro-plugins
git init
git add .
git commit -m "Initial commit: Custom registration plugin for Open edX"
git remote add origin https://github.com/tu-usuario/tutor-customregistration.git
git push -u origin main
```

### 2. En tu MV de Azure

#### Conectarse al servidor
```bash
ssh tu-usuario@tu-servidor-azure.com
```

#### Clonar el plugin
```bash
cd /home/tu-usuario/  # O donde tengas instalado Tutor
git clone https://github.com/tu-usuario/tutor-customregistration.git
cd tutor-customregistration
```

#### Instalar el plugin
```bash
# Para Tutor 19.0.0, verificar que el entorno virtual esté activo
which tutor
tutor --version  # Debe mostrar 19.0.0

# Instalar plugin
pip install -e .
```

#### Habilitar plugin
```bash
tutor plugins enable customregistration
tutor plugins list  # Verificar que aparece
```

#### Configurar MFE (IMPORTANTE)
```bash
# Configurar para que el MFE reconozca los campos
tutor config save --set MFE_CONFIG='{"ENABLE_DYNAMIC_REGISTRATION_FIELDS": true}'
```

#### Construir imágenes (ESTO TARDA)
```bash
# Esto puede tardar 20-30 minutos
tutor images build openedx
```

#### Ejecutar migraciones de BD
```bash
# Para Tutor 19.0.0, usar el comando simplificado
tutor local do init --limit=openedx-lms
```

#### Reiniciar todo
```bash
tutor local restart
```

### 3. Verificación

#### Comprobar que funciona
```bash
# Ver logs en tiempo real para debug
tutor local logs lms -f

# En otra terminal, prueba registrarte en:
# https://tu-dominio.com/register
```

#### Si hay problemas con el CURP/validaciones
```bash
# Ver logs específicos
tutor local logs lms | grep "customregistration"
tutor local logs lms | grep "CURP"
```

### 4. Configuración de tu MFE Fork

Asegúrate de que tu MFE (frontend-app-authn) esté configurado para apuntar a tu servidor:

#### En tu config.yml de Tutor
```yaml
MFE_CONFIG:
  ENABLE_DYNAMIC_REGISTRATION_FIELDS: true
  # Si tienes tu propio fork del MFE:
  # MFE_AUTHN_REPOSITORY: "https://github.com/tu-usuario/emi-frontend-app-authn.git"
  # MFE_AUTHN_VERSION: "main"
```

### 5. Testing del Payload

Una vez todo instalado, cuando alguien se registre, deberías ver en los logs algo como:

```
[customregistration] Registration attempt with custom fields: ['primer_apellido', 'segundo_apellido', 'numero_telefono', 'estado', 'municipio', 'nombre_escuela', 'cct', 'grado', 'curp']
[customregistration] Custom profile created successfully for user: nuevo_usuario
```

### 6. Acceso al Admin Django

Para ver los datos registrados:
```
https://tu-dominio.com/admin/customregistration/usercustomprofile/
```

### 7. Si necesitas hacer cambios

```bash
# En tu máquina local, hacer cambios y subir
git add .
git commit -m "Fix: algún cambio"
git push

# En el servidor Azure
cd tutor-customregistration
git pull
tutor local restart  # Solo si cambios menores
# Si cambios mayores: tutor images build openedx && tutor local restart
```

### Comandos de Emergencia

Si algo sale mal:
```bash
# Desactivar plugin temporalmente
tutor plugins disable customregistration
tutor local restart

# Reactivar
tutor plugins enable customregistration  
tutor local restart

# Ver todos los plugins
tutor plugins list

# Ver configuración completa
tutor config printroot
cat $(tutor config printroot)/config.yml
```

### Datos de Testing

Para probar el registro, usa datos como:
- **CURP**: `GALJ850315HDFRPR09`
- **CCT**: `12ABC3456D`
- **Teléfono**: `5512345678`
- **Estado**: `Ciudad de México`
- **Municipio**: `Benito Juárez`

¡Esto debería funcionar con tu setup actual en Azure! 🚀
