from rest_framework import serializers

from .models import PRDeployment


class PRDeploymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PRDeployment
        fields = (
            'id',
            'image',
            'log',
            'port',
            'succeeded',
        )
