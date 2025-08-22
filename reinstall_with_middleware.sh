#!/bin/bash
echo "🔧 Reinstalando plugin con middleware para capturar datos..."
echo "⚠️  Base de datos externa detectada - usando configuración Tutor"

cd /opt/registro-plugins

# 1. Desinstalar plugin actual
echo "1. Deshabilitando plugin actual..."
sudo tutor plugins disable customregistration
sudo tutor config save

# 2. Reinstalar plugin
echo "2. Reinstalando plugin..."
sudo pip install -e .

# 3. Habilitar plugin
echo "3. Habilitando plugin con middleware..."
sudo tutor plugins enable customregistration
sudo tutor config save

# 4. Reiniciar servicios
echo "4. Reiniciando LMS..."
sudo tutor local restart lms

echo ""
echo "✅ Plugin reinstalado con middleware para auth_userprofile"
echo ""
echo "🧪 Para probar:"
echo "1. Registra un nuevo usuario con datos mexicanos"
echo "2. Verifica con:"
echo "   chmod +x check_userprofile_data.sh"
echo "   ./check_userprofile_data.sh"
echo ""
echo "📊 Ver logs del middleware:"
echo "   sudo tutor local logs lms | grep tutorcustomregistration"
echo ""
echo "🔍 Verificación manual:"
echo "   sudo tutor local exec lms python manage.py dbshell"
echo "   SELECT au.username, au.first_name, au.last_name, aup.name, aup.phone_number, aup.meta FROM auth_user au LEFT JOIN auth_userprofile aup ON au.id = aup.user_id WHERE au.date_joined >= DATE_SUB(NOW(), INTERVAL 10 MINUTE) ORDER BY au.date_joined DESC;"
