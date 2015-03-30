# -*- coding: utf8 -*-
from datetime import timedelta

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.shortcuts import render
from django.utils.timezone import now

from frigg.builds.models import Build, Project


@staff_member_required
def overview(request):
    graph_top = 0
    builds_per_day = {'labels': [], 'values': [], 'succeeded': []}
    if 'psycopg2' in settings.DATABASES['default']['ENGINE']:
        data = Build.objects.filter(start_time__gte=(now() - timedelta(weeks=30))) \
                            .extra({"day": "date_trunc('day', start_time)"}) \
                            .values("day").order_by("day").annotate(count=Count("id"))

        for point in data:
            graph_top = max([graph_top, point['count']])
            builds_per_day['labels'].append(point['day'].day)
            builds_per_day['values'].append(point['count'])

    pending_builds = Build.objects.filter(result=None)

    return render(request, 'stats/overview.html', {
        'number_of_builds': Build.objects.all().count(),
        'number_of_success': Build.objects.filter(result__succeeded=True).count(),
        'number_of_failure': Build.objects.filter(result__succeeded=False).count(),
        'number_of_pending': len(pending_builds),
        'approved_projects': Project.objects.filter(approved=True).count(),
        'unapproved_projects': Project.objects.filter(approved=False).count(),
        'builds_per_day': builds_per_day,
        'graph_top': graph_top,
        'pending_builds': pending_builds
    })
