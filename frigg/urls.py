# coding=utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'frigg.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^github-webhook/', 'frigg.builds.views.github_webhook'),
    url(r'^admin/', include(admin.site.urls)),
)
