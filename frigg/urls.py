# -*- coding: utf8 -*-
from django.conf.urls import include, patterns, url
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

urlpatterns = patterns(
    'frigg.builds.api',
    url(r'^api/workers/report/$', 'report_build', name='worker_api_report_build'),
    url(r'^badges/coverage/(?P<owner>[^/]+)/(?P<project>[^/]+)/$', 'coverage_badge',
        name='coverage_badge'),
    url(r'^badges/coverage/(?P<owner>[^/]+)/(?P<project>[^/]+)/(?P<branch>[^/]+)/$',
        'coverage_badge', name='coverage_badge'),
    url(r'^badges/(?P<owner>[^/]+)/(?P<project>[^/]+)/$', 'build_badge', name='build_badge'),
    url(r'^badges/(?P<owner>[^/]+)/(?P<project>[^/]+)/(?P<branch>[^/]+)/$', 'build_badge',
        name='build_badge'),
)

urlpatterns += patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^webhooks/', include('frigg.webhooks.urls', namespace='webhooks', app_name='webhooks')),

    url(r'^auth/login/?$', RedirectView.as_view(url='/auth/login/github/'), name='login'),
    url(
        r'^auth/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'
    ),
    url(r'^auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'stats/', include('frigg.stats.urls', namespace='stats')),
    url(r'^', include('frigg.builds.urls')),
)
