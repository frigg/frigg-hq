# -*- coding: utf8 -*-
import json

from django.http import HttpResponse, Http404
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from frigg.decorators import token_required
from .models import Build, Project


@token_required
@csrf_exempt
def report_build(request):
    try:
        payload = json.loads(str(request.body, encoding='utf-8'))
        build = Build.objects.get(pk=payload['id'])
        build.handle_worker_report(payload)
        response = JsonResponse({'message': 'Thanks for building it'})
    except Build.DoesNotExist:
        response = JsonResponse({'error': 'Build not found'})
        response.status_code = 404
    return response


@never_cache
@csrf_exempt
def build_badge(request, owner, project, branch='master'):
    project = get_object_or_404(Project, owner=owner, name=project)
    badge = project.get_badge(branch)
    if badge is None:
        raise Http404

    return HttpResponse(content=badge, content_type='image/svg+xml')
