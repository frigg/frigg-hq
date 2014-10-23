# -*- coding: utf8 -*-
from functools import wraps

from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt


def token_required(view_func):
    @csrf_exempt
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.META.get('HTTP_FRIGG_WORKER_TOKEN')
        if token:
            if token in getattr(settings, 'FRIGG_WORKER_TOKENS', []):
                return view_func(request, *args, **kwargs)
        return HttpResponseForbidden
    return _wrapped_view
