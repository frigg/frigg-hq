# -*- coding: utf8 -*-
import os

from django.conf.global_settings import (TEMPLATE_CONTEXT_PROCESSORS as
                                         DJANGO_TEMPLATE_CONTEXT_PROCESSORS)
from django.contrib import messages

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'v8aa$cb0knx6)vyo!%tn6k6_g($!n1yq_v+4bg9v4*n@&dpu0w'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
INTERNAL_IPS = ('127.0.0.1:8000',)

MESSAGE_TAGS = {
    messages.ERROR: 'danger'  # Makes messages play nice with bootstrap 3
}


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'social_auth',

    'frigg.builds'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (DJANGO_TEMPLATE_CONTEXT_PROCESSORS +
                               ('django.core.context_processors.debug',))

ROOT_URLCONF = 'frigg.urls'

WSGI_APPLICATION = 'frigg.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.contrib.github.GithubBackend',
    'django.contrib.auth.backends.ModelBackend',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_ROOT = os.path.join(BASE_DIR, '../static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../uploads')
MEDIA_URL = '/uploads/'
STATICFILES_DIRS = os.path.join(BASE_DIR, 'files/'),


# Social auth
LOGIN_URL = '/auth/login/github'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/auth/error/'

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ENABLED_BACKENDS = 'github',

GITHUB_EXTENDED_PERMISSIONS = ['repo', 'read:org']
