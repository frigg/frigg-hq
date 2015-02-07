# -*- coding: utf8 -*-
from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect

from .models import Build, Project


def overview(request, page=1):
    projects_to_approve = Project.objects.permitted(request.user).filter(approved=False).count()

    if projects_to_approve > 0:
        messages.info(request, 'One or more projects needs approval before any builds will run.')

    build_list = Build.objects.permitted(request.user).select_related('project', 'result')
    paginator = Paginator(build_list, settings.OVERVIEW_PAGINATION_COUNT)

    try:
        builds = paginator.page(page)
    except EmptyPage:
        raise Http404

    return render(request, "builds/overview.html", {
        'projects_to_approve': projects_to_approve,
        'builds': builds
    })


def approve_projects(request, project_id=None):

    if not request.user.is_superuser:
        raise Http404

    if project_id and request.method == 'POST' and request.POST.get('approve') == "yes":
        project = Project.objects.get(id=project_id)
        project.approved = True
        project.save()

        if project.builds.all():
            project.builds.last().start()

        return redirect('approve_projects_overview')

    return render(request, "builds/approve_projects.html", {
        'projects': Project.objects.filter(approved=False)
    })


def view_organization(request, owner):
    builds = Build.objects.permitted(request.user) \
        .filter(project__owner=owner) \
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


def download_artifact(request, owner, name, artifact):
    if not Project.objects.permitted(request.user).filter(owner=owner, name=name).exists():
        raise Http404

    response = HttpResponse()
    response['X-Accel-Redirect'] = '/protected' + request.path_info
    response['Content-Disposition'] = 'attachment; filename="%s"' % artifact
    return response
