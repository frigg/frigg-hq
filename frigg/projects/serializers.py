from rest_framework import serializers

from frigg.builds.serializers import BuildInlineSerializer

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    builds = BuildInlineSerializer(read_only=True, many=True)

    class Meta:
        model = Project
        fields = (
            'id',
            'owner',
            'name',
            'private',
            'approved',
            'builds'
        )
