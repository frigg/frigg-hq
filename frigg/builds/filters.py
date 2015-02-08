from rest_framework import filters
from frigg.builds.models import Project, Build


class ProjectPermissionFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Project.objects.permitted_query(request.user))


class BuildPermissionFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(Build.objects.permitted_query(request.user))
