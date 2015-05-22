# -*- coding: utf8 -*-
from django.http import Http404, HttpResponse

from .models import Project


def download_artifact(request, owner, name, artifact):
    if not Project.objects.permitted(request.user).filter(owner=owner, name=name).exists():
        raise Http404

    response = HttpResponse()
    response['X-Accel-Redirect'] = '/protected' + request.path_info
    response['Content-Disposition'] = 'attachment; filename="%s"' % artifact
    return response
