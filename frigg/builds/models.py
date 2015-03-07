# -*- coding: utf8 -*-
import json
import logging
import re
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

from frigg.helpers import github
from frigg.helpers.badges import get_badge, get_coverage_badge

from .managers import BuildManager, BuildResultManager, ProjectManager

logger = logging.getLogger(__name__)


class Project(TimeStampModel):
    name = models.CharField(max_length=100, blank=True)
    owner = models.CharField(max_length=100, blank=True)
    git_repository = models.CharField(max_length=150)
    average_time = models.IntegerField(null=True)
    private = models.BooleanField(default=True, db_index=True)
    approved = models.BooleanField(default=False, db_index=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='projects', null=True,
                                     blank=True)
    objects = ProjectManager()

    class Meta:
        ordering = ['owner', 'name']

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

    def start_build(self, data):
        if 'message' not in data:
            data['message'] = None
        if 'author' not in data:
            data['author'] = ''

        return Build.objects.create(
            project=self,
            build_number=self.last_build_number + 1,
            pull_request_id=data['pull_request_id'],
            branch=data['branch'],
            sha=data['sha'],
            author=data['author'],
            message=data['message']
        ).start()

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

    @classmethod
    def token_for_url(cls, repo_url):
        try:
            project = Project.objects.get(git_repository=repo_url)
            token = project.github_token
        except cls.DoesNotExist:
            token = getattr(settings, 'GITHUB_ACCESS_TOKEN', ':')
        return token


class Build(TimeStampModel):
    project = models.ForeignKey(Project, related_name='builds', null=True)
    build_number = models.IntegerField(db_index=True)
    pull_request_id = models.IntegerField(max_length=150, default=0)
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
        return '%s / %s' % (self.project, self.branch)

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
        if self.is_pending:
            return 'orange'
        if self.result.succeeded:
            return 'green'
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
        self.save()

        r = redis.Redis(**settings.REDIS_SETTINGS)
        r.lpush(settings.FRIGG_WORKER_QUEUE, json.dumps(self.queue_object))

        return self

    def has_timed_out(self):
        used_time = now() - self.start_time
        if self.project.average_time:
            return (used_time > timedelta(seconds=self.project.average_time * 2) or
                    used_time > timedelta(minutes=10))
        else:
            return used_time > timedelta(minutes=10)

    def handle_worker_report(self, payload):
        logger.info('Handle worker report: %s' % payload)
        BuildResult.create_from_worker_payload(self, payload)

        github.set_commit_status(self)
        self.end_time = now()
        self.save()

        if 'webhooks' in payload:
            for url in payload['webhooks']:
                self.send_webhook(url)

    def send_webhook(self, url):
        return requests.post(url, data=json.dumps({
            'repository': self.project.git_repository,
            'sha': self.sha,
            'build_url': self.get_absolute_url(),
            'pull_request_id': self.pull_request_id,
            'state': self.result.succeeded,
            'return_code': self.result.return_code
        }), headers={'content-type': 'application/json'})


class BuildResult(TimeStampModel):
    build = models.OneToOneField(Build, related_name='result')
    result_log = models.TextField()
    succeeded = models.BooleanField(default=False)
    return_code = models.CharField(max_length=100)
    coverage = models.DecimalField(max_digits=5, decimal_places=2, editable=False, null=True,
                                   blank=True)

    objects = BuildResultManager()

    def __str__(self):
        return '%s - %s' % (self.build, self.build.build_number)

    @property
    def return_codes(self):
        return [int(code) for code in self.return_code.split(',')]

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
        return re.findall(
            r'Task: ([\w&=_\-\*\.\:\;\|/ ]+)\n\n------------------------------------\n'
            r'((?:(?!Task:).*\n)*)'
            r'------------------------------------\nExited with exit code: (\d*)\n\n',
            str(self.result_log)
        )

    @classmethod
    def create_not_approved(cls, build):
        result = cls.objects.create(build=build, result_log='This project is not approved.',
                                    succeeded=False)
        github.set_commit_status(build, error='This project is not approved')
        return result

    @classmethod
    def create_from_worker_payload(cls, build, payload):
        result = cls.objects.get_or_create(build_id=build.pk)[0]
        return_codes = []
        for r in payload['results']:
            if 'return_code' in r:
                return_codes.append(r['return_code'])
            result.result_log += cls.create_log_string_for_task(r)

        result.succeeded = BuildResult.evaluate_results(payload['results'])
        result.return_code = ",".join([str(code) for code in return_codes])
        if 'coverage' in payload:
            result.coverage = payload['coverage']
        result.save()

    @classmethod
    def evaluate_results(cls, results):
        succeeded = True
        for r in results:
            if 'succeeded' in r:
                succeeded = succeeded and r['succeeded']
        return succeeded

    @classmethod
    def create_log_string_for_task(cls, result):
        data = {'task': '', 'log': '', 'return_code': ''}
        data.update(result)

        return ('Task: %(task)s\n'
                '\n------------------------------------\n'
                '%(log)s'
                '\n------------------------------------\n'
                'Exited with exit code: %(return_code)s\n\n') % data
