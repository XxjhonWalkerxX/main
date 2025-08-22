# Tutor Plugin for Custom Mexican Registration Fields

Plugin simple para Open edX que agrega campos de registro mexicanos.

## Campos incluidos

- `primer_apellido` - Primer Apellido
- `segundo_apellido` - Segundo Apellido  
- `numero_telefono` - Número de Teléfono
- `estado` - Estado
- `municipio` - Municipio
- `nombre_escuela` - Nombre de la Escuela
- `cct` - CCT (Centro de Trabajo)
- `grado` - Grado
- `curp` - CURP

## Instalación

```bash
# Instalar el plugin
sudo pip install -e .

# Habilitar el plugin
sudo tutor plugins enable customregistration
sudo tutor config save

# Reiniciar servicios
sudo tutor local restart lms
```

## Verificación

Ejecuta el script de verificación:

```bash
chmod +x check_userprofile_data.sh
./check_userprofile_data.sh
```

Los datos se guardan en:
- `auth_user.first_name` y `auth_user.last_name` (nombres básicos)
- `auth_userprofile.meta` (todos los datos como JSON)
- `auth_userprofile.phone_number`, `auth_userprofile.state`, etc.

## Estructura

- `tutorcustomregistration/plugin.py` - Configuración principal del plugin
- `tutorcustomregistration/middleware.py` - Middleware para capturar y guardar datos
- `check_userprofile_data.sh` - Script para verificar datos guardados
- `reinstall_with_middleware.sh` - Script para reinstalar el plugin
