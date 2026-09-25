#!/bin/bash
# Script de inicio para AppWeb (Django) con Gunicorn en servidor Linux
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

python manage.py collectstatic --noinput
python manage.py migrate --noinput
exec gunicorn REQ_NLP.wsgi:application --bind=0.0.0.0:8000