import json
from datetime import timedelta

import redis
from django.conf import settings
from django.db import models
from django.utils.timezone import now

from frigg.helpers import github

from .managers import PRDeploymentManager


class PRDeployment(models.Model):
    build = models.OneToOneField('builds.Build', related_name='deployment', unique=True)
    port = models.IntegerField()
    image = models.CharField(max_length=255, default=settings.FRIGG_PREVIEW_IMAGE)
    log = models.TextField(blank=True)
    succeeded = models.NullBooleanField()
    docker_id = models.CharField(max_length=150, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)

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
        if self.build.project.owner == 'frigg':
            return 86400
        # This value should be calculated based on the owner
        return 1800

    @property
    def is_alive(self):
        if self.start_time is None:
            return False
        return bool(self.succeeded) and self.start_time + timedelta(seconds=self.ttl) > now()

    @property
    def is_pending(self):
        return self.succeeded is None

    @property
    def queue_object(self):
        obj = self.build.queue_object

        obj.update({
            'id': self.pk,
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
        github.set_commit_status(self.build, pending=True, context='frigg-preview')
        self.start_time = now()
        self.save()

    def stop(self):
        r = redis.Redis(**settings.REDIS_SETTINGS)
        r.lpush('frigg:queue:pr-deployments', json.dumps({
            'stop': True,
            'docker_id': self.docker_id
        }))

    def handle_report(self, payload):
        self.log = json.dumps(payload['results'])
        self.succeeded = True
        if 'docker_id' in payload:
            self.docker_id = payload['docker_id']

        for result in payload['results']:
            if 'pending' in result and result['pending']:
                self.succeeded = None
                break

            if result['succeeded'] is False:
                self.succeeded = False
                break

        self.save()

        if self.succeeded is True or self.succeeded is False:
            github.set_commit_status(self.build, context='frigg-preview')
