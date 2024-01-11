from .base import *
import dj_database_url

#DEBUG = 'RENDER' not in os.environ

ALLOWED_HOSTS = []

"""
ALLOWED_HOSTS = ['127.0.0.1',
    NGROK_URL_S, #esta es la direccion a cambiar por el ngrok, sin https
    '127.0.0.1:4040']
"""

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default='postresql://postgres:postgres@localhost/postgres',
        conn_max_age=600
    )
}

#STATICFILES_DIR = (BASE_DIR,'media/')
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"