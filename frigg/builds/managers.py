from django.core.cache import cache
from django.db.models import Q

from frigg.projects.managers import PermittedManager


class BuildManager(PermittedManager):

    def permitted_query(self, user):
        query = Q(project__private=False)
        if user.is_authenticated():
            projects = cache.get('projects:permitted:{}'.format(user.username))
            if projects is None:
                from frigg.builds.models import Project  # isort:skip # noqa
                projects = [p.pk for p in Project.objects.permitted(user)]
                cache.set('projects:permitted:{}'.format(user.username), projects, 60 * 10)
            query = Q(project_id__in=projects)
        return query


class BuildResultManager(PermittedManager):

    def permitted_query(self, user):
        query = Q(build__project__private=False)
        if user.is_authenticated():
            query |= Q(build__project__members=user)
        return query
