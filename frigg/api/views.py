from rest_framework import viewsets

from frigg.builds.filters import ProjectPermissionFilter, BuildPermissionFilter
from frigg.builds.models import Project, Build
from frigg.builds.serializers import ProjectSerializer, PaginatedBuildSerializer, BuildSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [ProjectPermissionFilter]


class BuildViewSet(viewsets.ModelViewSet):
    queryset = Build.objects.all()
    serializer_class = BuildSerializer
    pagination_serializer_class = PaginatedBuildSerializer
    paginate_by = 50
    filter_backends = [BuildPermissionFilter]
