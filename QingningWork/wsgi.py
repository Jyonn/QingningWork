"""
WSGI config for QingningWork project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import django.conf
from django.core.handlers.wsgi import WSGIHandler

django.conf.ENVIRONMENT_VARIABLE = 'DJANGO_QINGNINGWORK_SETTINGS_MODULE'

os.environ.setdefault("DJANGO_QINGNINGWORK_SETTINGS_MODULE", "QingningWork.settings")

application = WSGIHandler()
