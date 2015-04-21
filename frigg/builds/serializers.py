from rest_framework import serializers

from .models import Build, BuildResult, Project


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
