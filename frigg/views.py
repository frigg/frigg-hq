# -*- coding: utf-8 -*-
import json
import subprocess

from django.conf import settings
from django.core.cache import cache
from django.shortcuts import render
from django.views.decorators.cache import cache_control

from frigg.authentication.serializers import UserSerializer


def react_view(request):
    return render(request, 'react-base.html', {
        'user': json.dumps(UserSerializer(request.user).data),
        'sentry_dsn': getattr(settings, 'JS_SENTRY_DSN', '')
    })


@cache_control(private=True)
def offline_manifest(request):
    version = cache.get('gitrev')
    if not version:
        version = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        cache.set('gitrev', version, 60 * 15)
    return render(request, 'offline.manifest', {'version': version},
                  content_type='text/cache-manifest')
