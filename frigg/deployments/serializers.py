from rest_framework import serializers

from frigg.builds.serializers import BuildSerializer
from frigg.projects.models import Project


class PRDeploymentSerializer(serializers.ModelSerializer):
    build = BuildSerializer

    class Meta:
        model = Project
        fields = (
            'id',
            'build',
            'name',
            'log',
            'port',
            'succeeded',
        )
