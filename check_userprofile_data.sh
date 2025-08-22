#!/bin/bash
echo "🔍 Verificando datos en auth_userprofile..."
echo "==========================================="

echo "1. Usuarios recientes y sus profiles:"
echo "------------------------------------"
sudo tutor local exec lms python manage.py dbshell << 'EOF'
SELECT 
    au.username,
    au.first_name,
    au.last_name,
    au.email,
    au.date_joined,
    aup.name as profile_name,
    aup.phone_number,
    aup.state,
    aup.city,
    aup.meta
FROM auth_user au
LEFT JOIN auth_userprofile aup ON au.id = aup.user_id
WHERE au.date_joined >= DATE_SUB(NOW(), INTERVAL 2 HOUR)
ORDER BY au.date_joined DESC
LIMIT 5;
EOF

echo ""
echo "2. Buscar datos mexicanos en campo meta:"
echo "---------------------------------------"
sudo tutor local exec lms python manage.py dbshell << 'EOF'
SELECT 
    au.username,
    au.email,
    au.date_joined,
    aup.name,
    aup.phone_number,
    aup.state,
    aup.city,
    aup.meta
FROM auth_user au
JOIN auth_userprofile aup ON au.id = aup.user_id
WHERE au.date_joined >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
  AND (
    aup.meta LIKE '%primer_apellido%' OR
    aup.meta LIKE '%curp%' OR
    aup.meta LIKE '%cct%' OR
    aup.phone_number IS NOT NULL AND aup.phone_number != ''
  )
ORDER BY au.date_joined DESC;
EOF

echo ""
echo "3. Contar profiles recientes:"
echo "----------------------------"
sudo tutor local exec lms python manage.py dbshell << 'EOF'
SELECT COUNT(*) as profiles_recientes
FROM auth_user au
JOIN auth_userprofile aup ON au.id = aup.user_id
WHERE au.date_joined >= DATE_SUB(NOW(), INTERVAL 24 HOUR);
EOF
