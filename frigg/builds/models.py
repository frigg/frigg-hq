# -*- coding: utf8 -*-
import json
import logging
import re
import redis

import requests
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from social_auth.db.django_models import UserSocialAuth

from frigg.helpers import github
from frigg.helpers.badges import get_badge
from .managers import ProjectManager, BuildManager, BuildResultManager


logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class Project(models.Model):
    name = models.CharField(max_length=100, blank=True)
    owner = models.CharField(max_length=100, blank=True)
    git_repository = models.CharField(max_length=150)
    average_time = models.IntegerField(null=True)
    private = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='authx1_projects', null=True,
                             blank=True, help_text='A user with access to the repository.')

    objects = ProjectManager()

    def __str__(self):
        return "%(owner)s / %(name)s " % self.__dict__

    @property
    def github_token(self):
        try:
            token = UserSocialAuth.objects.get(user=self.user,
                                               provider='github').extra_data['access_token']
        except UserSocialAuth.DoesNotExist:
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
        return Build.objects.create(
            project=self,
            build_number=self.last_build_number + 1,
            pull_request_id=data['pull_request_id'],
            branch=data['branch'],
            sha=data["sha"]
        ).start()

    def get_badge(self, branch='master'):
        build = self.builds.filter(branch=branch).exclude(result=None).first()
        if build:
            return get_badge(build.result.succeeded)

    @classmethod
    def token_for_url(cls, repo_url):
        try:
            project = Project.objects.get(git_repository=repo_url)
            token = project.github_token
        except cls.DoesNotExist:
            token = getattr(settings, 'GITHUB_ACCESS_TOKEN', ':')
        return token


@python_2_unicode_compatible
class Build(models.Model):
    project = models.ForeignKey(Project, related_name='builds', null=True)
    build_number = models.IntegerField(db_index=True)
    pull_request_id = models.IntegerField(max_length=150, default=0)
    branch = models.CharField(max_length=100, default="master")
    sha = models.CharField(max_length=150)

    objects = BuildManager()

    class Meta:
        unique_together = ('project', 'build_number')
        ordering = ['-id']

    def __str__(self):
        return "%s / %s " % (self.project, self.branch)

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
    def color(self):
        if self.is_pending:
            return 'orange'
        if self.result.succeeded:
            return 'green'
        return 'red'

    @property
    def comment_message(self):
        if self.succeeded:
            return "All gooodie good\n\n%s" % self.get_absolute_url()
        else:
            return "Be careful.. the tests failed\n\n%s" % self.get_absolute_url()

    @property
    def queue_object(self):
        return {
            'id': self.pk,
            'branch': self.branch,
            'sha': self.sha,
            'clone_url': self.project.clone_url,
            'owner': self.project.owner,
            'name': self.project.name
        }

    def start(self):
        if hasattr(self, 'result'):
            self.result.delete()

        if not self.project.approved:
            BuildResult.create_not_approved(self)
            return self

        github.set_commit_status(self, pending=True)

        r = redis.Redis(**settings.REDIS_SETTINGS)
        r.lpush(settings.FRIGG_WORKER_QUEUE, json.dumps(self.queue_object))

        return self

    def handle_worker_report(self, payload):
        logger.info('Handle worker report: %s' % payload)
        BuildResult.create_from_worker_payload(self, payload)

        github.set_commit_status(self)
        if 'comment' in payload and payload['comment']:
            github.comment_on_commit(self, self.comment_message)

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
        }))


@python_2_unicode_compatible
class BuildResult(models.Model):
    build = models.OneToOneField(Build, related_name='result')
    result_log = models.TextField()
    succeeded = models.BooleanField(default=False)
    return_code = models.CharField(max_length=100)

    objects = BuildResultManager()

    def __str__(self):
        return '%s - %s' % (self.build, self.build.build_number)

    @property
    def return_codes(self):
        return [int(code) for code in self.return_code.split(',')]

    @property
    def tasks(self):
        return re.findall(
            r'Task: ([a-zA-Z0-9_\- ]+)\n\n------------------------------------\n'
            r'((?:(?!Task:).*\n)*)'
            r'------------------------------------\nExited with exit code: (\d+)',
            str(self.result_log)
        )

    @classmethod
    def create_not_approved(cls, build):
        cls.objects.create(build=build, result_log='This project is not approved.', succeeded=False)
        github.set_commit_status(build, error='This project is not approved')

    @classmethod
    def create_from_worker_payload(cls, build, payload):
        result = cls.objects.create(build_id=build.pk, return_code='', result_log='')
        return_codes = []
        for r in payload['results']:
            if 'return_code' in r:
                return_codes.append(r['return_code'])
            result.result_log += cls.create_log_string_for_task(r)

        result.succeeded = BuildResult.evaluate_results(payload['results'])
        result.return_code = ",".join([str(code) for code in return_codes])
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
