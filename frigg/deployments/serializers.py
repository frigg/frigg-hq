from rest_framework import serializers

from .models import PRDeployment


class PRDeploymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PRDeployment
        fields = (
            'id',
            'image',
            'tasks',
            'port',
            'succeeded',
            'start_time',
            'ttl',
            'is_pending',
            'is_alive'
        )
