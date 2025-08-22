#!/bin/bash
echo "🔧 Reinstalando plugin con HOOKS (Opción 2)..."
echo "⚠️  Usando hooks en lugar de middleware para evitar errores"

cd /opt/registro-plugins

# 1. Desinstalar plugin actual
echo "1. Deshabilitando plugin actual..."
sudo tutor plugins disable customregistration
sudo tutor config save

# 2. Reinstalar plugin
echo "2. Reinstalando plugin con hooks..."
sudo pip install -e .

# 3. Habilitar plugin
echo "3. Habilitando plugin con procesamiento por hooks..."
sudo tutor plugins enable customregistration
sudo tutor config save

# 4. Reiniciar servicios
echo "4. Reiniciando LMS..."
sudo tutor local restart lms

echo ""
echo "✅ Plugin reinstalado con hooks de Tutor (SIN middleware)"
echo ""
echo "🎯 CÓMO FUNCIONA AHORA:"
echo "- Usa signals de Django + monkey patching"
echo "- NO requiere middleware en el contenedor"
echo "- Intercepta el registro y guarda en auth_userprofile"
echo ""
echo "🧪 Para probar:"
echo "1. Registra un nuevo usuario con datos mexicanos"
echo "2. Verifica con:"
echo "   chmod +x check_userprofile_data.sh"
echo "   ./check_userprofile_data.sh"
echo ""
echo "📊 Ver logs:"
echo "   sudo tutor local logs lms | grep tutorcustomregistration"
