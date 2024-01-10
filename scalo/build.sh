#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install -r requirements.txt

python manage.py collectstatic --no-input

python manage.py makemigrations

python manage.py migrate

# Crear superusuario (reemplaza 'tunombredeusuario', 'tuemail' y 'tupassword' con los valores deseados)
#echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('lospitudos', 'reservatotalsa@gmail.com', 'aguantelvalo')" | python manage.py shell