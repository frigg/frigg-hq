# -*- coding: utf8 -*-
from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.core.paginator import EmptyPage, Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Build, Project


def overview(request, page=1):
    projects_to_approve = cache.get('projects:unapproved:count')
    if projects_to_approve is None:
        projects_to_approve = Project.objects.permitted(request.user).filter(approved=False).count()
        cache.set('projects:unapproved:count', projects_to_approve, 60 * 60 * 24)

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

    success_rate = 0
    if len(builds):
        success_rate = int((builds.filter(result__succeeded=True).count()/len(builds)) * 100)

    return render(request, "builds/organization.html", {
        'organization': owner,
        'builds': builds,
        'success_rate': success_rate
    })


def view_project(request, owner, name):
    project = get_object_or_404(
        Project.objects.permitted(request.user).prefetch_related('builds', 'builds__result'),
        owner=owner,
        name=name
    )
    builds = project.builds.all().select_related('project', 'result')

    success_rate = 0
    if len(builds):
        success_rate = int((builds.filter(result__succeeded=True).count()/len(builds)) * 100)

    return render(request, "builds/project.html", {
        'project': project,
        'builds': builds,
        'success_rate': success_rate
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
