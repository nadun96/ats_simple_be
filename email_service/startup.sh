#!/bin/bash

# Wait for database to be ready
echo "Waiting for database to be ready..."
python -c "
import os
import time
import psycopg2
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Wait for database connection
max_attempts = 30
attempt = 0
while attempt < max_attempts:
    try:
        import django
        django.setup()
        from django.db import connection
        connection.ensure_connection()
        print('Database connection successful!')
        break
    except Exception as e:
        print(f'Database not ready (attempt {attempt + 1}/{max_attempts}): {e}')
        time.sleep(2)
        attempt += 1
else:
    print('Could not connect to database after maximum attempts')
    exit(1)
"

echo "Creating migrations..."
python manage.py makemigrations api

echo "Applying migrations..."
python manage.py migrate

echo "Loading email templates..."
python manage.py load_email_templates

echo "Starting Django server..."
python manage.py runserver 0.0.0.0:8002
