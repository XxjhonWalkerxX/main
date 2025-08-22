#!/bin/bash
echo "🚨 ARREGLANDO ERROR DE MIDDLEWARE..."
echo "=================================="

cd /opt/registro-plugins

echo "1. Deshabilitando plugin para arreglar LMS..."
sudo tutor plugins disable customregistration
sudo tutor config save

echo "2. Reinstalando plugin sin middleware..."
sudo pip install -e .

echo "3. Habilitando plugin corregido..."
sudo tutor plugins enable customregistration
sudo tutor config save

echo "4. Reiniciando LMS (esto puede tardar)..."
sudo tutor local restart lms

echo ""
echo "✅ LMS debería funcionar ahora (sin middleware)"
echo ""
echo "🎯 PRÓXIMOS PASOS:"
echo "1. Verificar que el LMS funcione: http://tu-dominio"
echo "2. El registro funcionará pero SIN guardar datos custom aún"
echo "3. Necesitamos implementar una solución diferente al middleware"
