from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from .projects import views as project_views
from . import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^webhooks/', include('frigg.webhooks.urls', namespace='webhooks', app_name='webhooks')),

    url(
        r'^badges/coverage/(?P<owner>[^/]+)/(?P<name>[^/]+)/$',
        project_views.coverage_badge,
        name='coverage_badge'
    ),
    url(
        r'^badges/coverage/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<branch>[^/]+)/$',
        project_views.coverage_badge,
        name='coverage_badge'
    ),
    url(
        r'^badges/(?P<owner>[^/]+)/(?P<name>[^/]+)/$',
        project_views.build_badge,
        name='build_badge'
    ),
    url(
        r'^badges/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<branch>[^/]+)/$',
        project_views.build_badge,
        name='build_badge'
    ),

    url(
        r'^auth/login/?$',
        RedirectView.as_view(url='/auth/login/github/', permanent=False),
        name='login'
    ),
    url(
        r'^auth/logout/$',
        auth_views.logout,
        {'next_page': '/'},
        name='logout'
    ),
    url(r'^auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^stats/', include('frigg.stats.urls', namespace='stats')),
    url(r'^api/', include('frigg.api.urls', namespace='api')),
    url(r'^', include('frigg.projects.urls')),
    url(r'^', include('frigg.builds.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + [
    url(r'^[^/]+/[^/]+/[^/]+/$', views.react_view),
    url(r'^[^/]+/[^/]+/$', views.react_view),
    url(r'^[^/]+/$', views.react_view),
    url(r'^$', views.react_view, name='react_view'),
]
