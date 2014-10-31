# -*- coding: utf8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'frigg.stats.views',

    url(r'^$', 'overview', name='overview'),
)
