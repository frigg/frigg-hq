from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect

from .models import Project


def last_build(request, owner, name):
    project = get_object_or_404(Project.objects.permitted(request.user), owner=owner, name=name)
    return redirect(project.builds.first())


def download_artifact(request, owner, name, artifact):
    if not Project.objects.permitted(request.user).filter(owner=owner, name=name).exists():
        raise Http404

    response = HttpResponse()
    response['X-Accel-Redirect'] = '/protected' + request.path_info
    response['Content-Disposition'] = 'attachment; filename="%s"' % artifact
    return response
