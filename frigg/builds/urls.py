from django.conf.urls import patterns, url


urlpatterns = patterns(
    'frigg.builds.views',

    url(r'^$', 'overview', name='overview'),
    url(
        r'^(?P<owner>[^/]+)/$',
        'view_organization',
        name="view_organization"
    ),
    url(
        r'^(?P<owner>[^/]+)/(?P<name>[^/]+)/$',
        'view_project',
        name="view_project"
    ),
    url(
        r'^(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<build_number>\d+)/$',
        'view_build',
        name="view_build"
    ),

    url(r'^deploy/(?P<build_id>\d+)/$', 'deploy_master_branch', name="deploy_master_branch"),
)
