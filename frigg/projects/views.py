from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt

from .models import Project


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
