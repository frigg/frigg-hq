# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.shortcuts import render

from frigg.authentication.serializers import UserSerializer


def react_view(request):
    return render(request, 'react-base.html', {
        'user': json.dumps(UserSerializer(request.user).data),
        'sentry_dsn': getattr(settings, 'JS_SENTRY_DSN', '')
    })
