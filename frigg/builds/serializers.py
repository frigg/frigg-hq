from rest_framework import serializers

from .models import Build, BuildResult, Project


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id',
            'owner',
            'name',
            'private',
            'approved',
            'git_repository'
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


class BuildSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
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
