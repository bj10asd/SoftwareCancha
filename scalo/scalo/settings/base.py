"""
Django settings for scalo project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from django.conf import settings
import os


NGROK_URL_S = "f19e-2803-9800-b402-7ed6-b465-647-3310-e878.ngrok-free.app"
NGROK_URL = "https://"+ NGROK_URL_S

# SDK de Mercado Pago
#import mercadopago
# Agrega credenciales
#sdk = mercadopago.SDK("APP_USR-5356790108164574-102419-d8674a362fdf8c1bedf821d8159c1d3e-1522412137")
YOUR_PUBLIC_KEY="APP_USR-49830c2d-5e11-4c81-a9e9-4fd2fc139e92"
YOUR_ACCESS_TOKEN="APP_USR-5356790108164574-102419-d8674a362fdf8c1bedf821d8159c1d3e-1522412137"
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-013b_+ub)1bho77vrq+7tkwmqnjct)=!8b!kw#^92lmaxrtu#x'
SECRET_KEY = os.environ.get('SECRET_KEY', default='your secret key')

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True
#DEBUG = 'RENDER' not in os.environ


"""
ALLOWED_HOSTS = ['127.0.0.1',
    NGROK_URL_S, #esta es la direccion a cambiar por el ngrok, sin https
    '127.0.0.1:4040']
"""

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reservas',
    'django_plotly_dash.apps.DjangoPlotlyDashConfig',
    'channels',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_plotly_dash.middleware.BaseMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'scalo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'scalo.wsgi.application'

"""
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379),],
        },
    },
}
"""
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

X_FRAME_OPTIONS = 'SAMEORIGIN'
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'es-ar'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'America/Argentina/Salta'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder'
]

PLOTLY_COMPONENTS = [

    'dash_core_components',
    'dash_html_components',
    'dash_renderer',

    'dpd_components'
]


#STATIC_URL = 'static/'
#STATIC_ROOT = ''
#STATIC_URL = '/static/'

#STATIC_ROOT = ''
STATIC_URL = '/static/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

# This setting tells Django at which URL static files are going to be served to the user.
# Here, they well be accessible at your-domain.onrender.com/static/...

# Following settings only make sense on production and may break development environments.
#if not DEBUG:    # Tell Django to copy statics to the `staticfiles` directory
    # in your application directory on Render.
STATIC_ROOT = os.path.join(BASE_DIR, STATIC_URL)
    # Turn on WhiteNoise storage backend that takes care of compressing static files
    # and creating unique names for each version so they can safely be cached forever.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#MEDIA_URL = 'reservas/static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / MEDIA_URL

CSRF_TRUSTED_ORIGINS = [NGROK_URL]


#Mails
EMAIL_HOST = 'smtp.googlemail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'reservatotalsa@gmail.com'
EMAIL_HOST_PASSWORD = 'ahmw xfoz coiz zhvz'
EMAIL_USE_TLS = True