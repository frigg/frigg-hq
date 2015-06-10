from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from frigg.builds.models import Build

from .models import Project


def view_organization(request, owner):
    if request.user.is_staff:
        return redirect('/beta/{0}'.format(owner))

    builds = Build.objects.permitted(request.user) \
        .filter(project__owner=owner) \
        .select_related('project', 'result__still_running', 'result__succeeded')

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
    if request.user.is_authenticated():
        return redirect('/beta/{0}/{1}'.format(owner, name))

    project = get_object_or_404(
        Project.objects.permitted(request.user).prefetch_related('builds', 'builds__result'),
        owner=owner,
        name=name
    )
    builds = project.builds.all() \
        .select_related('project', 'result__still_running', 'result__succeeded')

    success_rate = 0
    if len(builds):
        success_rate = int((builds.filter(result__succeeded=True).count()/len(builds)) * 100)

    return render(request, "builds/project.html", {
        'project': project,
        'builds': builds,
        'success_rate': success_rate
    })


@never_cache
@csrf_exempt
def build_badge(request, owner, name, branch='master'):
    project = get_object_or_404(Project, owner=owner, name=name)
    badge = project.get_badge(branch)
    return HttpResponse(content=badge, content_type='image/svg+xml')


@never_cache
@csrf_exempt
def coverage_badge(request, owner, name, branch='master'):
    project = get_object_or_404(Project, owner=owner, name=name)
    badge = project.get_coverage_badge(branch)
    return HttpResponse(content=badge, content_type='image/svg+xml')


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
