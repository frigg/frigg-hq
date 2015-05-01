from rest_framework import serializers

from frigg.projects.models import Project

from .models import Build, BuildResult


class ProjectInlineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id',
            'owner',
            'name',
            'private',
            'approved',
        )


class BuildResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = BuildResult
        fields = (
            'id',
            'coverage',
            'succeeded',
            'tasks',
        )


class BuildInlineSerializer(serializers.ModelSerializer):
    result = BuildResultSerializer(read_only=True)

    class Meta:
        model = Build
        fields = (
            'id',
            'build_number',
            'branch',
            'sha',
            'pull_request_id',
            'start_time',
            'end_time',
            'result'
        )


class BuildSerializer(serializers.ModelSerializer):
    project = ProjectInlineSerializer(read_only=True)
    result = BuildResultSerializer(read_only=True)

    class Meta:
        model = Build
        fields = (
            'id',
            'project',
            'result',
            'build_number',
            'branch',
            'pull_request_id',
            'sha',
            'start_time',
            'end_time',
        )
