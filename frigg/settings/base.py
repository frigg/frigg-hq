# -*- coding: utf8 -*-
import os

from django.conf.global_settings import \
    TEMPLATE_CONTEXT_PROCESSORS as DJANGO_TEMPLATE_CONTEXT_PROCESSORS
from django.contrib import messages

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'v8aa$cb0knx6)vyo!%tn6k6_g($!n1yq_v+4bg9v4*n@&dpu0w'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []
INTERNAL_IPS = ('127.0.0.1',)

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

    'social.apps.django_app.default',
    'pipeline',
    'django_extensions',
    'rest_framework',
    'cachalot',

    'frigg.authentication',
    'frigg.builds',
    'frigg.stats',
    'frigg.webhooks',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    DJANGO_TEMPLATE_CONTEXT_PROCESSORS + (
        'django.core.context_processors.debug',
        'django.core.context_processors.request',
        'social.apps.django_app.context_processors.backends',
        'social.apps.django_app.context_processors.login_redirect',
    )
)

ROOT_URLCONF = 'frigg.urls'

WSGI_APPLICATION = 'frigg.wsgi.application'

AUTH_USER_MODEL = 'authentication.User'
AUTHENTICATION_BACKENDS = (
    'social.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'frigg',
        'HOST': '127.0.0.1'
    }
}

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = False
USE_TZ = True
DATETIME_FORMAT = 'Y-m-d H:i'

STATIC_ROOT = os.path.join(BASE_DIR, '../static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, '../uploads')
MEDIA_URL = '/uploads/'
STATICFILES_DIRS = os.path.join(BASE_DIR, 'files/'),
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE_COMPILERS = (
    'pipeline.compilers.sass.SASSCompiler',
)
PIPELINE_CSS = {
    'main': {
        'source_filenames': (
            'sass/main.sass',
        ),
        'output_filename': 'css/main.css',
    },
}


# Social auth
LOGIN_URL = '/auth/login/github'
LOGIN_REDIRECT_URL = '/'
LOGIN_ERROR_URL = '/auth/error/'


# python social auth
SOCIAL_AUTH_URL_NAMESPACE = 'social'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
SOCIAL_AUTH_GITHUB_SCOPE = ['repo', 'read:org']
