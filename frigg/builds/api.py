# -*- coding: utf8 -*-
import json

from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from frigg.decorators import token_required

from frigg.helpers import github
from .models import Project, Build


@csrf_exempt
def github_webhook(request):
    try:
        event = request.META['HTTP_X_GITHUB_EVENT']
    except KeyError:
        return HttpResponse("Missing HTTP_X_GITHUB_EVENT")

    data = json.loads(request.body)
    if event == "issue_comment":
        data = github.parse_comment_payload(data)

        # if this comment is on a pull request, build it
        if data and data['pull_request_url'] != "":
            data = github.parse_pull_request_payload(github.api_request(
                data['pull_request_url'],
                Project.token_for_url(data['repo_url'])
            ))

    elif event == "pull_request":
        data = github.parse_pull_request_payload(data)

    elif event == "push":
        data = github.parse_push_payload(data)

    else:
        return HttpResponse("Unknown event: %s" % event)

    if data:
        project = Project.objects.get_or_create_from_url(data['repo_url'])
        project.private = data['private']
        project.save()
        build = project.start_build(data)
        return HttpResponse('Handled "%s" event.\nMore info at %s' % (
            event,
            build.get_absolute_url())
        )
    else:
        return HttpResponse('Handled "%s" event.' % event)


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
