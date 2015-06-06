from rest_framework import serializers

from frigg.deployments.serializers import PRDeploymentSerializer
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
            'setup_tasks',
            'still_running',
        )


class BuildInlineSerializer(serializers.ModelSerializer):
    result = BuildResultSerializer(read_only=True)
    deployment = PRDeploymentSerializer(read_only=True)

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
            'result',
            'short_message',
            'message',
            'author',
            'color',
            'pull_request_url',
            'commit_url',
            'deployment',
        )


class BuildSerializer(serializers.ModelSerializer):
    project = ProjectInlineSerializer(read_only=True)
    result = BuildResultSerializer(read_only=True)
    deployment = PRDeploymentSerializer(read_only=True)

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
            'short_message',
            'message',
            'author',
            'color',
            'pull_request_url',
            'commit_url',
            'deployment',
        )
