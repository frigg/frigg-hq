# -*- coding: utf8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from frigg.builds.models import Build, Project


@staff_member_required
def overview(request):
    return render(request, 'stats/overview.html', {
        'number_of_builds': Build.objects.all().count(),
        'number_of_success': Build.objects.filter(result__succeeded=True).count(),
        'number_of_failure': Build.objects.filter(result__succeeded=False).count(),
        'number_of_pending': Build.objects.filter(result=None).count(),
        'approved_projects': Project.objects.filter(approved=True).count(),
        'unapproved_projects': Project.objects.filter(approved=False).count(),
    })
