# -*- coding: utf-8 -*-
import subprocess

from django.contrib.admin.views.decorators import staff_member_required
from django.core.cache import cache
from django.shortcuts import render
from django.views.decorators.cache import cache_control


@staff_member_required
def react_view(request):
    return render(request, 'react-base.html')


@cache_control(private=True)
def offline_manifest(request):
    version = cache.get('gitrev')
    if not version:
        version = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
        cache.set('gitrev', version, 60 * 15)
    return render(request, 'offline.manifest', {'version': version},
                  content_type='text/cache-manifest')
