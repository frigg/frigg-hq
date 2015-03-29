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
    if event == 'ping':
        data = github.parse_ping_payload(data)
        if data is None:
            return HttpResponse('Organization ping event received')
        project = Project.objects.get_or_create_from_url(data['repo_url'])
        project.private = data['private']
        try:
            user = get_user_model().objects.get(username=project.owner)

            # Must add a user before checking for more
            project.members.add(user)
            project.update_members()
        except get_user_model().DoesNotExist:
            if data['private'] is False:
                project.update_members()
        project.save()
        return HttpResponse('Added project %s' % project)

    elif event == 'issue_comment':
        data = github.parse_comment_payload(data)

    elif event == 'pull_request':
        data = github.parse_pull_request_payload(data)

    elif event == 'push':
        data = github.parse_push_payload(data)

    elif event == 'member':
        if data['action'] != 'added':
            # no other action is supported so we don't know how the payload will be
            return HttpResponse('Unknown action')

        data = github.parse_member_payload(data)
        if get_user_model().objects.filter(username=data['username']).exists():
            project = Project.objects.get(name=data['repo_name'], owner=data['repo_owner'])
            project.members.add(get_user_model().objects.get(username=data['username']))
            return HttpResponse('Added %s to the project' % data['username'])
        return HttpResponse('Unknown user %s' % data['username'])

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
    return HttpResponse('Could not handle event')
