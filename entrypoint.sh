#!/bin/bash
set -e


poetry run python manage.py makemigrations --noinput
poetry run python manage.py migrate --noinput


poetry run python manage.py shell << EOF
from django.contrib.auth import get_user_model

User = get_user_model()
if not User.objects.filter(username='test').exists():
    User.objects.create_superuser('test', 'test@example.com', 'testtest')

EOF

exec poetry run python manage.py runserver 0.0.0.0:8000
