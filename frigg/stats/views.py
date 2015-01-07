# -*- coding: utf8 -*-
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import render
from django.utils.timezone import now
from frigg.builds.models import Build, Project


@staff_member_required
def overview(request):
    builds_per_day = {'labels': [], 'values': [], 'succeeded': []}
    data = Build.objects.filter(start_time__gte=(now() - timedelta(weeks=30))) \
                        .extra({"day": "date_trunc('day', start_time)"}) \
                        .values("day").order_by("day").annotate(count=Count("id"))

    for point in data:
        builds_per_day['labels'].append(point['day'].day)
        builds_per_day['values'].append(point['count'])

    return render(request, 'stats/overview.html', {
        'number_of_builds': Build.objects.all().count(),
        'number_of_success': Build.objects.filter(result__succeeded=True).count(),
        'number_of_failure': Build.objects.filter(result__succeeded=False).count(),
        'number_of_pending': Build.objects.filter(result=None).count(),
        'approved_projects': Project.objects.filter(approved=True).count(),
        'unapproved_projects': Project.objects.filter(approved=False).count(),
        'builds_per_day': builds_per_day
    })
