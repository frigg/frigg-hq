# -*- coding: utf8 -*-
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Build, Project


@login_required
def overview(request):
    return render(request, "builds/overview.html", {
        'builds': Build.objects.all().order_by('-id').select_related('project', 'result')[:100]
    })


@login_required
def view_organization(request, owner):
    builds = Build.objects.filter(project__owner=owner).select_related('project', 'result')
    if len(builds) == 0:
        raise Http404

    return render(request, "builds/organization.html", {
        'organization': owner,
        'builds': builds
    })


@login_required
def view_project(request, owner, name):
    return render(request, "builds/project.html", {
        'project': get_object_or_404(Project.objects.prefetch_related('builds'), owner=owner,
                                     name=name)
    })


@login_required
def view_build(request, owner, name, build_number):
    return render(request, "builds/build.html", {
        'build': get_object_or_404(Build.objects.select_related('project'), project__owner=owner,
                                   project__name=name, build_number=build_number)
    })


@login_required
def deploy_master_branch(request, build_id):
    build = Build.objects.get(id=build_id)
    build.deploy()

    return HttpResponse("Deployed")
