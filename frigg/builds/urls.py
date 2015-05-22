from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        r'^artifacts/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<artifact>.*)$',
        views.download_artifact,
        name='download_artifact'
    )
]
