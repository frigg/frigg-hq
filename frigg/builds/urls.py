from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.overview, name='overview'),
    url(r'^(?P<page>\d+)$', views.overview, name='overview'),
    url(r'^projects/approve/$', views.approve_projects, name='approve_projects_overview'),
    url(r'^projects/approve/(?P<project_id>\d+)/$', views.approve_projects, name='approve_project'),

    url(
        r'^(?P<owner>[^/]+)/$',
        views.view_organization,
        name='view_organization'
    ),
    url(
        r'^(?P<owner>[^/]+)/(?P<name>[^/]+)/$',
        views.view_project,
        name='view_project'
    ),
    url(
        r'^(?P<owner>[^/]+)/(?P<name>[^/]+)/last/$',
        views.last_build,
        name='last_build'
    ),
    url(
        r'^(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<build_number>\d+)/$',
        views.view_build,
        name='view_build'
    ),
    url(
        r'^artifacts/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<artifact>.*)$',
        views.download_artifact,
        name='download_artifact'
    )
]
