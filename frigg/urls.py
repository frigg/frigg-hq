from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^$', 'frigg.builds.views.overview'),

    url(
        r'^build/(?P<owner>[\w\.-_]+)/(?P<name>[\w\.-_]+)/(?P<build_number>\d+)/$',
        'frigg.builds.views.build',
        name="view_build"
    ),

    url(r'^deploy/(?P<build_id>\d+)/$', 'frigg.builds.views.deploy_master_branch',
        name="deploy_master_branch"),

    url(r'^github-webhook/', 'frigg.builds.views.github_webhook'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'},
        name='login'),

    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),
)
