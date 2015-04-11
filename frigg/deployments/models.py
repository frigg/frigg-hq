import json

import redis
from django.conf import settings
from django.db import models

from .managers import PRDeploymentManager


class PRDeployment(models.Model):
    build = models.OneToOneField('builds.Build', related_name='deployment', unique=True)
    port = models.IntegerField()
    image = models.CharField(max_length=255)
    log = models.TextField(blank=True)
    succeeded = models.NullBooleanField()

    objects = PRDeploymentManager()

    class Meta:
        verbose_name = 'Pull request deployment'
        verbose_name_plural = 'Pull request deployments'

    def __str__(self):
        return 'Deployment: {}'.format(self.build)

    def get_deployment_url(self):
        return 'http://{port}.pr.frigg.io'.format(port=self.port)

    @property
    def ttl(self):
        # This value should be calculated based on the owner
        return 1800

    @property
    def is_pending(self):
        return self.succeeded is None

    @property
    def queue_object(self):
        obj = self.build.queue_object
        obj.update({
            'port': self.port,
            'image': self.image,
            'ttl': self.ttl
        })
        return obj

    @property
    def tasks(self):
        return json.loads(self.log or '[]')

    def start(self):
        r = redis.Redis(**settings.REDIS_SETTINGS)
        r.lpush('frigg:queue:pr-deployments', json.dumps(self.queue_object))

    def handle_report(self, payload):
        self.log = json.dumps(payload['results'])
        self.succeeded = True

        for result in payload['results']:
            if result['succeeded'] is False:
                self.succeeded = False
                break

        self.save()
