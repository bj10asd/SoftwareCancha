"""
WSGI config for scalo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scalo.scalo.settings')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scalo.settings.local')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scalo.settings.production')

application = get_wsgi_application()
