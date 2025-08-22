# Tutor Plugin - Custom Registration Fields

Plugin de Tutor que agrega campos personalizados mexicanos al formulario de registro de Open edX.

## Descripción

Este plugin extiende el formulario de registro de Open edX para incluir campos específicos para usuarios mexicanos:

- **Primer Apellido** (requerido)
- **Segundo Apellido** (opcional)
- **Número de Teléfono** (10 dígitos)
- **Estado** (estado de residencia)
- **Municipio** (municipio de residencia)
- **Nombre de la Escuela** (institución educativa)
- **CCT** (Clave de Centro de Trabajo - 10 caracteres)
- **Grado** (grado escolar actual)
- **CURP** (Clave Única de Registro de Población - 18 caracteres)

## Características

### ✅ Validación de Campos
- **CURP**: Validación de formato mexicano oficial
- **CCT**: Validación de formato de Clave de Centro de Trabajo
- **Teléfono**: Validación de 10 dígitos
- **Unicidad**: El CURP debe ser único en el sistema

### ✅ Integración con Open edX
- Compatible con Open edX Sumac (19.0.0)
- Integración completa con Tutor
- Funciona con MFE de autenticación personalizado
- Almacenamiento seguro en base de datos

### ✅ Administración
- Interface de administración de Django
- Filtros y búsquedas por campos personalizados
- Validación automática de datos

## Instalación

### Prerrequisitos
- **Tutor 19.0.0** (Sumac)
- Open edX Sumac (19.0.0)
- MFE de authn personalizado configurado

### Pasos de Instalación

**Opción A: Instalar directamente desde GitHub**
```bash
pip install git+https://github.com/tu-usuario/tutor-customregistration.git
tutor plugins enable customregistration
tutor config save
tutor images build openedx
tutor local do init-customregistration
tutor local restart
```

**Opción B: Clonar e instalar localmente**
1. **Clonar el repositorio en tu MV**:
   ```bash
   git clone https://github.com/tu-usuario/tutor-customregistration.git
   cd tutor-customregistration
   ```

2. **Instalar el plugin**:
   ```bash
   pip install -e .
   ```

3. **Habilitar el plugin**:
   ```bash
   tutor plugins enable customregistration
   ```

4. **Configurar Tutor**:
   ```bash
   tutor config save
   ```

5. **Construir imágenes**:
   ```bash
   tutor images build openedx
   ```

6. **Ejecutar migraciones**:
   ```bash
   tutor local do init-customregistration
   ```

7. **Reiniciar servicios**:
   ```bash
   tutor local restart
   ```

## Configuración

### Configuración MFE
En tu configuración de Tutor, asegúrate de tener:

```yaml
MFE_CONFIG:
  ENABLE_DYNAMIC_REGISTRATION_FIELDS: true
```

### Configuración de Campos
Los campos se configuran automáticamente al habilitar el plugin. Los patrones de validación son:

- **CURP**: `^[A-Z]{4}[0-9]{6}[HM][A-Z]{5}[0-9]{2}$`
- **CCT**: `^[0-9]{2}[A-Z]{3}[0-9]{4}[A-Z]$`
- **Teléfono**: `^[0-9]{10}$`

## Uso

### Para Desarrolladores

#### Modelo de Datos
El plugin crea el modelo `UserCustomProfile` con relación uno-a-uno al modelo `User` de Django:

```python
from customregistration.models import UserCustomProfile

# Obtener perfil personalizado de un usuario
user = User.objects.get(username='student')
custom_profile = user.custom_profile
print(custom_profile.curp)
```

#### Señales Django
El plugin incluye señales para manejar la creación automática de perfiles:

```python
from customregistration.signals import save_custom_registration_data

# Guardar datos personalizados manualmente
custom_data = {
    'primer_apellido': 'García',
    'segundo_apellido': 'López',
    'curp': 'GALJ850315HDFRPR09',
    # ... otros campos
}
save_custom_registration_data(user, custom_data)
```

### Para Administradores

1. **Acceder al Admin de Django**:
   ```
   https://tu-sitio.com/admin/customregistration/usercustomprofile/
   ```

2. **Filtrar usuarios** por estado, municipio, grado, etc.

3. **Buscar usuarios** por CURP, nombre, escuela, etc.

## Estructura del Proyecto

```
tutorcustomregistration/
├── plugin.py                 # Configuración principal del plugin
├── templates/
│   └── customregistration/
│       ├── apps.py           # Configuración de la app Django
│       ├── models.py         # Modelos de datos
│       ├── views.py          # Vistas personalizadas
│       ├── admin.py          # Configuración del admin
│       ├── signals.py        # Señales Django
│       ├── urls.py           # URLs de la app
│       ├── migrations/       # Migraciones de DB
│       └── management/       # Comandos de gestión
└── setup.py                 # Configuración del paquete Python
```

## Validaciones y Seguridad

### Validaciones Frontend (MFE)
- Validación en tiempo real de campos
- Mensajes de error localizados
- Prevención de envío de formularios inválidos

### Validaciones Backend (Django)
- Validación de formatos mexicanos oficiales
- Verificación de unicidad de CURP
- Sanitización de datos de entrada
- Logging de errores y eventos

### Seguridad
- Protección CSRF habilitada
- Validación de entrada rigurosa
- Almacenamiento seguro en BD
- Logs de auditoría

## Troubleshooting

### Error: "CURP ya está registrado"
El CURP debe ser único. Verifica que no exista otro usuario con el mismo CURP.

### Error: "Formato de CCT inválido"
La CCT debe tener exactamente 10 caracteres en el formato: 2 números + 3 letras + 4 números + 1 letra.

### Error: "Plugin no encontrado"
Asegúrate de haber instalado el plugin correctamente:
```bash
pip install -e .
tutor plugins list
```

### Error de Migraciones
Si hay problemas con las migraciones:
```bash
tutor local run lms ./manage.py makemigrations customregistration
tutor local run lms ./manage.py migrate customregistration
```

## Desarrollo y Contribución

### Configuración de Desarrollo
1. Fork este repositorio
2. Crea un entorno virtual
3. Instala dependencias de desarrollo
4. Ejecuta las pruebas

### Ejecutar Pruebas
```bash
python -m pytest tests/
```

### Agregar Nuevos Campos
1. Modifica `models.py`
2. Crea nueva migración
3. Actualiza formularios MFE
4. Actualiza validaciones

## Licencia

MIT License - Ver archivo LICENSE para más detalles.

## Soporte

Para reportar problemas o solicitar características:
1. Crea un issue en el repositorio
2. Incluye logs relevantes
3. Describe los pasos para reproducir

---

**Versión**: 1.0.0  
**Compatibilidad**: Open edX Sumac (19.0.0), Tutor >= 15.0.0  
**Autor**: Diego Nicolas
