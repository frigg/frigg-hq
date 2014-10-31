# -*- coding: utf8 -*-
import json
from django.contrib.staticfiles import finders

from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from frigg.decorators import token_required
from .models import Build


@token_required
@csrf_exempt
def report_build(request):
    try:
        payload = json.loads(request.body)
        build = Build.objects.get(pk=payload['id'])
        build.handle_worker_report(payload)
        response = JsonResponse({'message': 'Thanks for building it'})
    except Build.DoesNotExist:
        response = JsonResponse({'error': 'Build not found'})
        response.status_code = 404
    return response


@csrf_exempt
def build_badge(request, owner, project, branch='master'):
    response = HttpResponse()
    try:
        build = Build.objects.filter(project__owner=owner, project__name=project, branch=branch)\
                             .exclude(result=None)[0]

        if build.result.succeeded:
            path = finders.find('badges/build-success.svg')
        else:
            path = finders.find('badges/build-failure.svg')

        with open(path) as f:
            response.content = f.read()
            response['Content-Type'] = 'image/svg+xml'

    except IndexError:
        response.status_code = 404

    return response
