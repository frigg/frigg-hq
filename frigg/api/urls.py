from django.conf.urls import include, url
from rest_framework import routers

from frigg.api.views import UserDetailView

from .views import BuildViewSet, ProjectViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'builds', BuildViewSet)

urlpatterns = [
    url(
        r'^builds/(?P<pk>\d+)/$',
        BuildViewSet.as_view({'get': 'retrieve'}),
        name='builds_by_owner'
    ),
    url(
        r'^builds/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<build_number>\d+)/$',
        BuildViewSet.as_view({'get': 'get_by_owner_name_build_number'}),
        name='build_by_owner_name_build_number'
    ),
    url(
        r'^builds/(?P<owner>[^/]+)/(?P<name>[^/]+)/$',
        BuildViewSet.as_view({'get': 'get_by_owner_name'}),
        name='builds_by_owner_name'
    ),
    url(
        r'^builds/(?P<owner>[^/]+)/$',
        BuildViewSet.as_view({'get': 'get_by_owner'}),
        name='builds_by_owner'
    ),
    url(
        r'^workers/report/$',
        'frigg.api.views.report_build',
        name='worker_api_report_build'
    ),
    url(
        r'^partials/build/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<build_number>\d+)/$',
        'frigg.api.views.partial_build_page',
        name='partial_build_page'
    ),
    url(
        r'^users/me/',
        UserDetailView.as_view(),
        name='user_me'
    ),
    url(
        r'^',
        include(router.urls)
    ),
]
