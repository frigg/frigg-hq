from rest_framework import permissions, viewsets

from frigg.api.permissions import ReadOnly
from frigg.builds.filters import BuildPermissionFilter, ProjectPermissionFilter
from frigg.builds.models import Build, Project
from frigg.builds.serializers import BuildSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [ProjectPermissionFilter]
    permission_classes = ReadOnly, permissions.DjangoModelPermissionsOrAnonReadOnly


class BuildViewSet(viewsets.ModelViewSet):
    queryset = Build.objects.all()
    serializer_class = BuildSerializer
    paginate_by = 50
    filter_backends = [BuildPermissionFilter]
    permission_classes = ReadOnly, permissions.DjangoModelPermissionsOrAnonReadOnly
