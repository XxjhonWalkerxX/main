# Configuración Completa MFE + Backend

## Tu Setup Actual:

### 🎯 Frontend (MFE) - YA TIENES
- ✅ Fork de `frontend-app-authn` con campos mexicanos
- ✅ Campos funcionando: primer_apellido, segundo_apellido, etc.
- ✅ Payload se envía correctamente al backend

### 🎯 Backend (Plugin) - RECIÉN CREADO
- ✅ Plugin Tutor 19.0.0 compatible
- ✅ Modelos Django para guardar campos
- ✅ Validaciones CURP, CCT, teléfono
- ✅ API endpoints para recibir datos del MFE

## Integración MFE ↔ Backend:

### 1. MFE envía campos via POST a `/api/user/v1/account/registration/`
```javascript
// Tu MFE ya hace esto:
const payload = {
  name: 'Juan',
  email: 'juan@email.com',
  username: 'juan123',
  password: '***',
  // Campos mexicanos:
  primer_apellido: 'García',
  segundo_apellido: 'López',
  numero_telefono: '5512345678',
  estado: 'CDMX',
  municipio: 'Benito Juárez',
  nombre_escuela: 'Secundaria Federal #1',
  cct: '09DES0001A',
  grado: '1° Secundaria',
  curp: 'GALJ850315HDFRPR09'
};
```

### 2. Backend recibe y procesa
```python
# El plugin hace esto automáticamente:
1. CustomRegistrationView recibe el POST
2. Valida campos con regex mexicanos
3. Crea User en Django
4. Crea UserCustomProfile con campos extra
5. Retorna success/error al MFE
```

### 3. Configuración requerida en tu MV
```yaml
# En config.yml de Tutor
MFE_CONFIG:
  ENABLE_DYNAMIC_REGISTRATION_FIELDS: true
```

## ¿Cómo conectar ambos?

### En tu MV de Azure:
1. **MFE personalizado** (que ya tienes) → se conecta automáticamente
2. **Instalar este plugin** → `pip install -e .`
3. **Configurar** → `tutor config save`
4. **Rebuil** → `tutor images build openedx`

### El flujo completo será:
```
Usuario llena formulario → MFE envía datos → Plugin recibe → Guarda en BD → Usuario creado
```

🎉 **¡Tu MFE y este backend son 100% compatibles!**
