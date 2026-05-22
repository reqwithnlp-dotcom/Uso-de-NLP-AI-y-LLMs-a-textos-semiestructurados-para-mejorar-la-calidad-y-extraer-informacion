FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias para MySQL
RUN apt-get update && apt-get install -y \
    libpq-dev gcc default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Copiar dependencias y instalarlas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY . .

# Recolectar archivos estáticos (para producción)
RUN python manage.py collectstatic --noinput

# Exponer el puerto
EXPOSE 8000

# Usar gunicorn en producción
CMD ["gunicorn", "REQ_NLP.wsgi:application", "--bind", "0.0.0.0:8000"]
