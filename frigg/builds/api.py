# -*- coding: utf8 -*-
import json

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .models import Build


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


def partial_build_page(request, owner, name, build_number):
    return render(request, 'builds/partials/build_result.html', {
        'build': get_object_or_404(
            Build.objects.select_related('result'),
            project__owner=owner,
            project__name=name,
            build_number=build_number
        )
    })
