from django.conf.urls import include, url
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectViewSet)
router.register(r'builds', views.BuildViewSet)

urlpatterns = [
    url(
        r'^builds/(?P<pk>\d+)/$',
        views.BuildViewSet.as_view({'get': 'retrieve'}),
        name='builds_by_owner'
    ),
    url(
        r'^builds/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<build_number>\d+)/$',
        views.BuildViewSet.as_view({'get': 'get_by_owner_name_build_number'}),
        name='build_by_owner_name_build_number'
    ),
    url(
        r'^builds/(?P<owner>[^/]+)/(?P<name>[^/]+)/$',
        views.BuildViewSet.as_view({'get': 'get_by_owner_name'}),
        name='builds_by_owner_name'
    ),
    url(
        r'^builds/(?P<owner>[^/]+)/$',
        views.BuildViewSet.as_view({'get': 'get_by_owner'}),
        name='builds_by_owner'
    ),
    url(
        r'^workers/report/$',
        views.report_build,
        name='worker_api_report_build'
    ),
    url(
        r'^deployments/report/$',
        views.report_deployment,
        name='worker_api_report_deployment'
    ),
    url(
        r'^partials/build/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<build_number>\d+)/$',
        views.partial_build_page,
        name='partial_build_page'
    ),
    url(
        r'^users/me/',
        views.UserDetailView.as_view(),
        name='user_me'
    ),
    url(
        r'^',
        include(router.urls)
    ),
]
