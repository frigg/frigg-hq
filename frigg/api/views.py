import json

from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from frigg.api.permissions import ReadOnly
from frigg.authentication.serializers import UserSerializer
from frigg.builds.filters import BuildPermissionFilter
from frigg.builds.models import Build, Project
from frigg.builds.serializers import BuildSerializer
from frigg.deployments.models import PRDeployment
from frigg.projects.filters import ProjectPermissionFilter
from frigg.projects.serializers import ProjectSerializer


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

    def get_builds(self, request):
        builds = Build.objects.permitted(request.user).select_related('project', 'result')[:50]
        return Response(BuildSerializer(builds, many=True).data)

    def get_by_owner(self, request, owner):
        builds = Build.objects.permitted(request.user).select_related('project', 'result').filter(
            project__owner=owner
        )[:100]

        if len(builds) == 0:
            raise Http404

        return Response(BuildSerializer(builds, many=True).data)

    def get_by_owner_name(self, request, owner, name):
        builds = Build.objects.permitted(request.user).select_related('project', 'result').filter(
            project__owner=owner,
            project__name=name
        )[:100]

        if len(builds) == 0:
            raise Http404

        return Response(BuildSerializer(builds, many=True).data)

    def get_by_owner_name_build_number(self, request, owner, name, build_number):
        build = get_object_or_404(
            Build.objects.permitted(request.user).select_related('project', 'result'),
            project__owner=owner,
            project__name=name,
            build_number=build_number
        )
        return Response(BuildSerializer(build).data)


class UserDetailView(APIView):
    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


@csrf_exempt
def report_build(request):
    try:
        payload = json.loads(str(request.body, encoding='utf-8'))
        build = Build.objects.get(pk=payload['id'])
        build.handle_worker_report(payload)
        response = JsonResponse({'message': 'Thanks for building it'})
    except Build.DoesNotExist:
        response = JsonResponse({'error': 'Build not found'})
        response.status_code = 404
    return response


@csrf_exempt
def report_deployment(request):
    try:
        payload = json.loads(str(request.body, encoding='utf-8'))
        deployment = PRDeployment.objects.get(pk=payload['id'])
        deployment.handle_report(payload)
        response = JsonResponse({'message': 'Thanks for deploying it'})
    except PRDeployment.DoesNotExist:
        response = JsonResponse({'error': 'Build not found'}, status=404)
    return response


def partial_build_page(request, owner, name, build_number):
    return render(request, 'builds/partials/build_result.html', {
        'build': get_object_or_404(
            Build.objects.select_related('result'),
            project__owner=owner,
            project__name=name,
            build_number=build_number
        )
    })
