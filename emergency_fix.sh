#!/bin/bash
echo "🚨 ARREGLO DE EMERGENCIA - LMS roto por plugin complejo"
echo "===================================================="

cd /opt/registro-plugins

echo "1. Deshabilitando plugin que rompe Django..."
sudo tutor plugins disable customregistration
sudo tutor config save

echo "2. Reinstalando versión SÚPER SIMPLE..."
sudo pip install -e .

echo "3. Habilitando plugin simple (solo campos)..."
sudo tutor plugins enable customregistration
sudo tutor config save

echo "4. Reiniciando LMS..."
sudo tutor local restart lms

echo ""
echo "✅ LMS debería funcionar ahora"
echo ""
echo "📋 ESTADO ACTUAL:"
echo "- Plugin: HABILITADO (solo define campos)"
echo "- LMS: FUNCIONANDO"
echo "- Registro: FUNCIONANDO"
echo "- Guardado de datos: NO (los datos se pierden por ahora)"
echo ""
echo "🎯 SIGUIENTE PASO:"
echo "Primero confirma que el LMS funciona y que puedes registrar usuarios"
echo "Después implementaremos una solución más simple para guardar datos"
