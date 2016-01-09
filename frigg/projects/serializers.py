from rest_framework import serializers

from frigg.builds.serializers import BuildInlineSerializer

from .models import Project


class EnvironmentVariableSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_secret:
            representation.value = '[secret]'
        return representation

    class Meta:
        model = Project
        fields = (
            'id',
            'key',
            'is_secret',
            'value',
        )


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
            'should_clone_with_ssh',
            'builds'
        )
