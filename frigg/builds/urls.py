from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^(?P<owner>[^/]+)/(?P<name>[^/]+)/last/$',
        views.last_build,
        name='last_build'
    ),
    url(
        r'^artifacts/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<artifact>.*)$',
        views.download_artifact,
        name='download_artifact'
    )
]
