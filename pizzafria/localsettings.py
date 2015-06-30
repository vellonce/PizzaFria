# -*- coding: utf-8 -*-
__author__ = 'iwdev1'

from .settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pizza_db',
        'USER': 'root',
        'PASSWORD': 'A8d32e08.',
        'HOST': '',
        'PORT': '',
    }
}

ALLOWED_HOSTS = []

STATIC_ROOT = ''

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates/static/'),
)