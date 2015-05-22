from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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
