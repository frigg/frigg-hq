from rest_framework import filters

from .models import Project


class ProjectPermissionFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Project.objects.permitted_query(request.user)).distinct()
