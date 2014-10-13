# -*- coding: utf8 -*-
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'v8aa$cb0knx6)vyo!%tn6k6_g($!n1yq_v+4bg9v4*n@&dpu0w'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

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

ROOT_URLCONF = 'frigg.urls'

WSGI_APPLICATION = 'frigg.wsgi.application'


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
