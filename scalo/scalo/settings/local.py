from .base import *


DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',
    NGROK_URL_S, #esta es la direccion a cambiar por el ngrok, sin https
    '127.0.0.1:4040']


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'    : 'django.db.backends.postgresql',
        'HOST'      : 'localhost',
        'PORT'      : 5432,
        #'NAME':     BASE_DIR / 'db.sqlite3',
        'NAME'      : 'Adsii',
        'USER'      : 'postgres',
        'PASSWORD'  : '1234'
    }
}