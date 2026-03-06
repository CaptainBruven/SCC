"""
Django settings for local development.

Usage:
    DJANGO_SETTINGS_MODULE=scc.settings.local python manage.py runserver
"""

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Debug toolbar (optional, add 'debug_toolbar' to INSTALLED_APPS if needed)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
# INTERNAL_IPS = ['127.0.0.1']
