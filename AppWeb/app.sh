cat << 'EOF' > app.sh
#!/bin/bash
python manage.py collectstatic --noinput
python manage.py migrate
exec gunicorn tu_proyecto.wsgi:application --bind=0.0.0.0:8080
EOF
chmod +x app.sh