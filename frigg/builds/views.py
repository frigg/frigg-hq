# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Build


@login_required
def overview(request):
    return render(request, "builds/overview.html", {
        'builds': Build.objects.all().order_by("-id").select_related('project', 'result')
    })


@login_required
def build(request, owner, name, build_number):
    return render(request, "builds/build.html", {
        'build': get_object_or_404(Build.objects.select_related('project'), project__owner=owner,
                                   project__name=name, build_number=build_number)
    })


@login_required
def deploy_master_branch(request, build_id):
    build = Build.objects.get(id=build_id)
    build.deploy()

    return HttpResponse("Deployed")


