# Guardado de Datos Personalizados - Sin Migraciones

## ✅ **Respuesta a tu pregunta:**

**NO necesitas migraciones** con la aproximación actual porque:

1. **Usamos el campo `meta` de UserProfile** (ya existe en Open edX)
2. **Es un campo JSON** que puede almacenar datos arbitrarios
3. **No creamos tablas nuevas**

## 🔄 **Cómo funciona:**

```python
# 1. Usuario se registra con campos mexicanos
POST /api/user/v2/account/registration/
{
  "username": "juan",
  "email": "juan@example.com", 
  "primer_apellido": "García",
  "curp": "GAJU801201HDFRNL05",
  ...
}

# 2. Open edX crea el usuario normal
User.objects.create(username="juan", email="juan@example.com")

# 3. Nuestro middleware guarda datos adicionales
UserProfile.objects.filter(user=user).update(meta={
  "primer_apellido": "García",
  "segundo_apellido": "López",
  "numero_telefono": "5551234567",
  "estado": "CDMX",
  "municipio": "Coyoacán", 
  "nombre_escuela": "Escuela Primaria Benito Juárez",
  "cct": "09DPR1234K",
  "grado": "6to",
  "curp": "GAJU801201HDFRNL05"
})
```

## 🚀 **Instalar versión actualizada:**

```bash
# 1. Detener Tutor
sudo tutor local stop

# 2. Copiar plugin actualizado
sudo cp -r /home/azureuser/registro-plugins /opt/
sudo chown -R root:root /opt/registro-plugins

# 3. Reinstalar
sudo tutor plugins uninstall customregistration  
sudo tutor plugins install /opt/registro-plugins

# 4. Rebuild
sudo tutor images build openedx

# 5. Iniciar
sudo tutor local start -d

# 6. Probar registro y consultar datos
sudo tutor local exec lms python /opt/registro-plugins/query_profiles.py
```

## 🎯 **Si más tarde quieres tabla dedicada:**

Entonces SÍ necesitarías migraciones:

```python
# En tutorcustomregistration/models.py
class UserCustomProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100, blank=True)
    # ... más campos
    
# Migración Django
python manage.py makemigrations tutorcustomregistration
python manage.py migrate
```

**Pero por ahora no es necesario.** La aproximación con `meta` es más simple y efectiva.
