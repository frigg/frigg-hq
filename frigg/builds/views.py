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

    build_list = Build.objects.permitted(request.user).select_related('project',
                                                                      'result__still_running',
                                                                      'result__succeeded')
    paginator = Paginator(build_list, settings.OVERVIEW_PAGINATION_COUNT)

    try:
        builds = paginator.page(page)
    except EmptyPage:
        raise Http404

    return render(request, "builds/overview.html", {
        'projects_to_approve': projects_to_approve,
        'builds': builds
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
