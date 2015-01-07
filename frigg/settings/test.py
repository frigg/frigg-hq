# -*- coding: utf8 -*-

PIPELINE_ENABLED = False
STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
