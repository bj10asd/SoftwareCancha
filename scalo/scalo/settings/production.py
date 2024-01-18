from .base import *
import dj_database_url

DEBUG =  True
ALLOWED_HOSTS = ['5inco.online']

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


"""if not DEBUG:    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'"""