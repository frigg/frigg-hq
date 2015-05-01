from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import RedirectView

from frigg.api.urls import router as api_router

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^webhooks/', include('frigg.webhooks.urls', namespace='webhooks', app_name='webhooks')),

    url(
        r'^api/workers/report/$',
        'frigg.builds.api.report_build',
        name='worker_api_report_build'
    ),
    url(
        r'^api/partials/build/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<build_number>\d+)/$',
        'frigg.builds.api.partial_build_page',
        name='api_partial_build_page'
    ),
    url(
        r'^badges/coverage/(?P<owner>[^/]+)/(?P<name>[^/]+)/$',
        'frigg.builds.api.coverage_badge',
        name='coverage_badge'
    ),
    url(
        r'^badges/coverage/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<branch>[^/]+)/$',
        'frigg.builds.api.coverage_badge',
        name='coverage_badge'
    ),
    url(
        r'^badges/(?P<owner>[^/]+)/(?P<name>[^/]+)/$',
        'frigg.builds.api.build_badge',
        name='build_badge'
    ),
    url(
        r'^badges/(?P<owner>[^/]+)/(?P<name>[^/]+)/(?P<branch>[^/]+)/$',
        'frigg.builds.api.build_badge',
        name='build_badge'
    ),

    url(
        r'^auth/login/?$',
        RedirectView.as_view(url='/auth/login/github/', permanent=False),
        name='login'
    ),
    url(
        r'^auth/logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': '/'},
        name='logout'
    ),
    url(r'^auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^auth/', include('django.contrib.auth.urls')),
    url(r'^stats/', include('frigg.stats.urls', namespace='stats')),
    url(r'^api/', include(api_router.urls)),
    url(r'^', include('frigg.builds.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
