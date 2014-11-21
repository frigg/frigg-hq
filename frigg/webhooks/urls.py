# -*- coding: utf8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'frigg.webhooks.views',
    url(r'^github/$', 'github_webhook', name='github'),
)
