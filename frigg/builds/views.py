# coding=utf-8
import json
import threading

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from frigg.helpers import github

from .models import Build, Project


@login_required
def overview(request):
    return render(request, "builds/overview.html", {'builds': Build.objects.all().order_by("-id")})


@login_required
def build(request, build_id):
    try:
        build = Build.objects.get(id=build_id)
        return render(request, "builds/build.html", {'build': build})

    except Build.DoesNotExist:
        raise Http404


@login_required
def deploy_master_branch(request, build_id):
    build = Build.objects.get(id=build_id)
    build.deploy()

    return HttpResponse("Deployed")

@csrf_exempt
def github_webhook(request):
    try:
        event = request.META['HTTP_X_GITHUB_EVENT']
    except KeyError:
        return HttpResponse("Missing HTTP_X_GITHUB_EVENT")

    data = json.loads(request.body)
    if event == "issue_comment":
        data = github.parse_comment_payload(data)

    elif event == "pull_request":
        data = github.parse_pull_request_payload(data)

    elif event == "push":
        data = github.parse_push_payload(data)

    else:
        return HttpResponse("Unknown event: %s" % event)

    if data:
        build = start_build(data)
        return HttpResponse(
            'Handled "%s" event.\nMore info at %s' % (event, build.get_absolute_url()))
    else:
        return HttpResponse('Handled "%s" event.' % event)


def start_build(data):
    project = Project.objects.get_or_create_from_url(data['repo_url'])
    build = Build.objects.create(
        project=project,
        build_number=project.last_build_number + 1,
        pull_request_id=data['pull_request_id'],
        branch=data['branch'],
        sha=data["sha"]
    )

    t = threading.Thread(target=build.run_tests)
    t.setDaemon(True)
    t.start()
    return build
