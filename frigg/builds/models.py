# -*- coding: utf8 -*-
import json
import logging
from datetime import timedelta

import redis
import requests
from basis.models import TimeStampModel
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.functional import cached_property
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from markdown import markdown

from frigg.deployments.models import PRDeployment
from frigg.helpers import github
from frigg.helpers.badges import get_badge, get_coverage_badge
from frigg.projects.managers import ProjectManager

from .managers import BuildManager, BuildResultManager

logger = logging.getLogger(__name__)


class Project(TimeStampModel):
    name = models.CharField(max_length=100, db_index=True, blank=True)
    owner = models.CharField(max_length=100, db_index=True, blank=True)
    private = models.BooleanField(default=True, db_index=True)
    approved = models.BooleanField(default=False, db_index=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='projects')
    queue_name = models.CharField(max_length=200, default=settings.FRIGG_WORKER_QUEUE)
    can_deploy = models.BooleanField(default=False, db_index=True)

    objects = ProjectManager()

    class Meta:
        ordering = ['owner', 'name']
        unique_together = ('owner', 'name')

    def __str__(self):
        return '%(owner)s / %(name)s' % self.__dict__

    def save(self, *args, **kwargs):
        cache.delete('projects:unapproved:count')
        if self.owner in settings.AUTO_APPROVE_OWNERS:
            self.approved = True
        super().save(*args, **kwargs)

    @property
    def github_token(self):
        try:
            token = self.members.first().github_token
        except AttributeError:
            token = None

        if not token:
            token = getattr(settings, 'GITHUB_ACCESS_TOKEN', ':')
        return token

    @property
    def clone_url(self):
        if self.private:
            return "https://%s@github.com/%s/%s" % (self.github_token, self.owner, self.name)
        else:
            return "https://github.com/%s/%s" % (self.owner, self.name)

    @property
    def last_build_number(self):
        try:
            return self.builds.all().order_by('-build_number')[0].build_number
        except IndexError:
            return 0

    @property
    def average_time(self):
        timings = []
        builds = self.builds.all()[:10]
        for build in builds:
            if build.start_time and build.end_time:
                timings.append((build.end_time - build.start_time).total_seconds())
        if timings:
            return timedelta(seconds=int(sum(timings) / len(timings)))

    def start_build(self, data):
        build_number = self.last_build_number + 1
        build, created = Build.objects.get_or_create(
            project=self,
            branch=data['branch'],
            sha=data['sha'],
            author=data['author'],
        )
        build.pull_request_id = data['pull_request_id']
        build.message = data['message']
        if created:
            build.build_number = build_number
        build.save()

        if created:
            build.start()

        return build

    def get_badge(self, branch='master'):
        build = self.builds.filter(branch=branch, pull_request_id=0).exclude(result=None).first()
        if build:
            return get_badge(build.result.succeeded)

    def get_coverage_badge(self, branch='master'):
        build = self.builds.filter(branch=branch, pull_request_id=0).exclude(result=None).first()
        if build:
            return get_coverage_badge(build.result.coverage)

    def update_members(self):
        collaborators = github.list_collaborators(self)
        users = get_user_model().objects.filter(username__in=collaborators)
        self.members = users


class Build(TimeStampModel):
    project = models.ForeignKey(Project, related_name='builds', null=True)
    build_number = models.IntegerField(default=0, null=True, db_index=True)
    pull_request_id = models.IntegerField(default=0)
    branch = models.CharField(max_length=100, default="master")
    sha = models.CharField(max_length=150)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    author = models.CharField(max_length=150, blank=True)
    message = models.TextField(null=True, blank=True, editable=False)

    objects = BuildManager()

    class Meta:
        unique_together = ('project', 'build_number')
        ordering = ['-id']

    def __str__(self):
        return '%s / %s #%s' % (self.project, self.branch, self.build_number)

    def get_absolute_url(self):
        return "https://%s%s" % (
            settings.SERVER_ADDRESS,
            reverse('view_build', args=[self.project.owner, self.project.name, self.build_number])
        )

    @property
    def pull_request_url(self):
        return github.get_pull_request_url(self)

    @property
    def commit_url(self):
        return github.get_commit_url(self)

    @property
    def is_pending(self):
        return not hasattr(self, 'result')

    @property
    def short_message(self):
        return self.message.split('\n')[0]

    @property
    def estimated_finish_time(self):
        if self.start_time and self.project.average_time:
            eta = self.start_time + self.project.average_time
            if now() < eta:
                return eta

    @property
    def rendered_message(self):
        return mark_safe(markdown(self.message, safe_mode='remove').replace('<p></p>', ''))

    @property
    def author_user(self):
        try:
            return get_user_model().objects.get(username=self.author)
        except get_user_model().DoesNotExist:
            return None

    @property
    def color(self):
        if self.is_pending or self.result.still_running:
            return 'orange'
        if self.result.succeeded:
            return 'green'
        if len(self.result.tasks) and self.result.tasks[0]['task'] == '':
            return 'gray'
        return 'red'

    @property
    def queue_object(self):
        obj = {
            'id': self.pk,
            'branch': self.branch,
            'sha': self.sha,
            'clone_url': self.project.clone_url,
            'owner': self.project.owner,
            'name': self.project.name,
        }
        if self.pull_request_id > 0:
            obj['pull_request_id'] = self.pull_request_id
        return obj

    def start(self):
        if hasattr(self, 'result'):
            self.result.delete()

        if not self.project.approved:
            BuildResult.create_not_approved(self)
            return self

        github.set_commit_status(self, pending=True)
        self.start_time = now()
        self.end_time = None
        self.save()

        r = redis.Redis(**settings.REDIS_SETTINGS)
        queue_length = r.lpush(self.project.queue_name, json.dumps(self.queue_object)) or 0

        if queue_length >= 10:
            logger.warning('Queue length exceeds 10 items')
        elif queue_length >= 5:
            logger.warning('Queue length exceeds 5 items')

        return self

    def has_timed_out(self):
        used_time = now() - self.start_time
        if self.project.average_time:
            return used_time > timedelta(seconds=self.project.average_time.total_seconds() * 2)
        else:
            return used_time > timedelta(minutes=60)

    def handle_worker_report(self, payload):
        logger.info('Handle worker report: %s' % payload)
        result = BuildResult.create_from_worker_payload(self, payload)
        if not result.still_running:
            github.set_commit_status(self)
            self.end_time = now()
            self.save()

            if self.project.can_deploy and self.pull_request_id:
                logger.warning('can deploy', extra=payload['settings'])
                if 'deployment' in payload['settings']:
                    self.initiate_deployment(payload['settings']['deployment'])

            if 'webhooks' in payload:
                for url in payload['webhooks']:
                    self.send_webhook(url)

    def send_webhook(self, url):
        return requests.post(url, data=json.dumps({
            'sha': self.sha,
            'build_url': self.get_absolute_url(),
            'pull_request_id': self.pull_request_id,
            'state': self.result.succeeded,
        }), headers={'content-type': 'application/json'})

    def initiate_deployment(self, options):
        PRDeployment.objects.get_or_create(
            build=self,
            image=options['image'],
            port=(self.pk % 64510) + 1024
        )[0].start()


class BuildResult(TimeStampModel):
    build = models.OneToOneField(Build, related_name='result')
    result_log = models.TextField()
    setup_log = models.TextField(blank=True)
    succeeded = models.BooleanField(default=False)
    still_running = models.BooleanField(default=False)
    coverage = models.DecimalField(max_digits=5, decimal_places=2, editable=False, null=True,
                                   blank=True)

    objects = BuildResultManager()

    def __str__(self):
        return str(self.build)

    @cached_property
    def coverage_diff(self):
        master_build = self.build.project.builds.filter(
            branch='master',
            end_time__lt=self.build.start_time
        ).exclude(result=None).first()
        if master_build:
            return self.coverage - (master_build.result.coverage or 0)
        return self.coverage

    @property
    def tasks(self):
        return json.loads(self.result_log)

    @property
    def setup_tasks(self):
        try:
            return json.loads(self.setup_log)
        except ValueError:
            return None

    @classmethod
    def create_not_approved(cls, build):
        result = cls.objects.create(
            build=build,
            result_log='[{"task": "", "error": "This project is not approved."}]',
            succeeded=False
        )
        github.set_commit_status(build, error='This project is not approved')
        return result

    @classmethod
    def create_from_worker_payload(cls, build, payload):
        result = cls.objects.get_or_create(build_id=build.pk)[0]
        result.result_log = json.dumps(payload['results'])
        if 'setup_results' in payload:
            result.setup_log = json.dumps(payload['setup_results'])
        result.succeeded = BuildResult.evaluate_results(payload['results'])

        if 'finished' in payload:
            result.still_running = not payload['finished']
        else:
            result.still_running = False

        if 'coverage' in payload:
            result.coverage = payload['coverage']

        result.save()
        return result

    @classmethod
    def evaluate_results(cls, results):
        succeeded = True
        for r in results:
            if 'succeeded' in r:
                succeeded = succeeded and r['succeeded']
        return succeeded
