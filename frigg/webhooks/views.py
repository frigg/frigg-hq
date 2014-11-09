# -*- coding: utf8 -*-
import json
from django.contrib.auth import get_user_model

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from frigg.builds.models import Project
from frigg.helpers import github


@csrf_exempt
def github_webhook(request):
    try:
        event = request.META['HTTP_X_GITHUB_EVENT']
    except KeyError:
        return HttpResponse('Missing HTTP_X_GITHUB_EVENT')

    data = json.loads(str(request.body, encoding='utf-8'))
    if event == 'issue_comment':
        data = github.parse_comment_payload(data)

        # if this comment is on a pull request, build it
        if data and data['pull_request_url'] != '':
            data = github.parse_pull_request_payload(github.api_request(
                data['pull_request_url'],
                Project.token_for_url(data['repo_url'])
            ))

    elif event == 'pull_request':
        data = github.parse_pull_request_payload(data)

    elif event == 'push':
        data = github.parse_push_payload(data)

    elif event == 'member':
        if data['action'] != 'added':
            # no other action is supported so we don't know how the payload will be
            return HttpResponse('Unknown action')

        username = data['member']['login']
        if get_user_model().objects.filter(username=username).exists():
            project = Project.objects.get(
                name=data['repository']['name'],
                owner=data['repository']['owner']['login']
            )
            project.members.add(get_user_model().objects.get(username=username))
            return HttpResponse('Added %s to the project' % data['member']['login'])
        return HttpResponse('Unknown user %s' % username)

    else:
        return HttpResponse('Unknown event: %s' % event)

    if data:
        project = Project.objects.get_or_create_from_url(data['repo_url'])
        project.private = data['private']
        project.save()
        build = project.start_build(data)
        return HttpResponse('Handled "%s" event.\nMore info at %s' % (
            event,
            build.get_absolute_url()
        ))
    else:
        return HttpResponse('Handled "%s" event.' % event)
