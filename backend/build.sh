#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='shaffaf@gmail.com').exists():
    User.objects.create_superuser(email='shaffaf@gmail.com', password='Shaffaf2025!', first_name='Shaffaf', last_name='Admin')
    print('Superuser yaradıldı')
else:
    print('Superuser artıq var')
"