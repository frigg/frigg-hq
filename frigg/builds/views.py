# -*- coding: utf8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from .models import Build, Project


def overview(request):
    projects_to_approve = Project.objects.permitted(request.user).filter(approved=False).count()

    return render(request, "builds/overview.html", {
        'projects_to_approve': projects_to_approve,
        'builds': Build.objects.permitted(request.user).order_by('-id')
                  .select_related('project', 'result')[:100]})


def approve_projects(request):
    if not request.user.is_superuser:
        raise Http404

    projects = Project.objects.permitted(request.user).filter(approved=False)
    return render(request, "builds/approve_projects.html", {'projects': projects})


def approve_project(request, id):
    if not request.user.is_superuser:
        raise Http404

    project = get_object_or_404(Project, id=id)
    project.approved = True
    project.save()

    return redirect(reverse(approve_projects))


def view_organization(request, owner):
    builds = Build.objects.permitted(request.user).filter(project__owner=owner) \
        .select_related('project', 'result')
    if len(builds) == 0:
        raise Http404

    return render(request, "builds/organization.html", {
        'organization': owner,
        'builds': builds
    })


def view_project(request, owner, name):
    return render(request, "builds/project.html", {
        'project': get_object_or_404(
            Project.objects.permitted(request.user).prefetch_related('builds'),
            owner=owner,
            name=name
        )
    })


def last_build(request, owner, name):
    project = get_object_or_404(Project.objects.permitted(request.user), owner=owner, name=name)
    return redirect(project.builds.first())


def view_build(request, owner, name, build_number):
    return render(request, "builds/build.html", {
        'build': get_object_or_404(
            Build.objects.permitted(request.user).select_related('project'),
            project__owner=owner,
            project__name=name,
            build_number=build_number
        )
    })
