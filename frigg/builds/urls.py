from django.conf.urls import patterns, url


urlpatterns = patterns(
    'frigg.builds.views',

    url(r'^$', 'overview'),
    url(
        r'^(?P<owner>[^/]+)/$',
        'organization',
        name="view_organization"
    ),
    url(
        r'^(?P<owner>[^/]+)/(?P<name>[^/]+)/$',
        'project',
        name="view_project"
    ),
    url(
        r'^(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<build_number>\d+)/$',
        'build',
        name="view_build"
    ),

    url(r'^deploy/(?P<build_id>\d+)/$', 'deploy_master_branch', name="deploy_master_branch"),
)
