from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^$',
        views.overview,
        name='overview'
    ),
    url(
        r'^(?P<page>\d+)$',
        views.overview,
        name='overview'
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
