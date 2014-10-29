# -*- coding: utf8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    'frigg.builds.api',
    url(r'^webhooks/github/$', 'github_webhook'),
    url(r'^api/workers/report/$', 'report_build', name='worker_api_report_build'),
    url(r'^badges/(?P<owner>[^/]+)/(?P<project>[^/]+)/$', 'build_badge', name='build_badge'),
    url(r'^badges/(?P<owner>[^/]+)/(?P<project>[^/]+)/(?P<branch>[^/]+)/$', 'build_badge',
        name='build_badge'),
)

urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),

    url(
        r'^auth/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': 'https://frigg.io'},
        name='logout'
    ),
    url(r'^auth/', include('social_auth.urls')),
    url(r'^', include('frigg.builds.urls')),
)
