# -*- coding: utf8 -*-
from django.conf.urls import patterns, url


urlpatterns = patterns(
    'frigg.builds.views',

    url(r'^$', 'overview', name='overview'),
    url(r'^(?P<page>\d+)$', 'overview', name='overview'),
    url(r'^approve/$', 'approve_projects', name='approve_projects'),

    url(
        r'^(?P<owner>[^/]+)/$',
        'view_organization',
        name='view_organization'
    ),
    url(
        r'^(?P<owner>[^/]+)/(?P<name>[^/]+)/$',
        'view_project',
        name='view_project'
    ),
    url(
        r'^(?P<owner>[^/]+)/(?P<name>[^/]+)/last/$',
        'last_build',
        name='last_build'
    ),
    url(
        r'^(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<build_number>\d+)/$',
        'view_build',
        name='view_build'
    ),
    url(
        r'^artifacts/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<artifact>.*)$',
        'download_artifact',
        name='download_artifact'
    )
)
