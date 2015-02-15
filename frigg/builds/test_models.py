# -*- coding: utf8 -*-
import json
from datetime import datetime, timedelta
from unittest import mock

import responses
from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.utils.timezone import get_current_timezone, now
from mockredis import mock_redis_client
from social.apps.django_app.default.models import UserSocialAuth

from .models import Build, BuildResult, Project


class ProjectTestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml']

    def tearDown(self):
        Project.objects.all().delete()

    def test___str__(self):
        project = Project.objects.create(owner='frigg', name='frigg-worker')
        self.assertEqual(str(project), 'frigg / frigg-worker')

    def test_create_project(self):
        url = 'git@github.com:tind/balder.git'
        project = Project.objects.get_or_create_from_url(url)
        self.assertEqual(project.owner, 'tind')
        self.assertEqual(project.name, 'balder')
        self.assertEqual(project.git_repository, url)
        self.assertIsNone(project.average_time)
        self.assertFalse(project.approved)
        self.assertEqual(Project.objects.all().count(), 1)

    def test_clone_url(self):
        project = Project.objects.create(owner='frigg', name='frigg-worker', private=False)
        self.assertEqual(project.clone_url, 'https://github.com/frigg/frigg-worker')
        project = Project.objects.create(owner='frigg', name='chewie', private=True)
        self.assertEqual(project.clone_url, 'https://@github.com/frigg/chewie')

    def test_last_build_number(self):
        project = Project.objects.create(owner='frigg', name='frigg-worker', private=False)
        self.assertEqual(project.last_build_number, 0)
        Build.objects.create(project=project, build_number=42)
        self.assertEqual(project.last_build_number, 42)

    def test_auto_approval(self):
        url = 'git@github.com:frigg/frigg.git'
        project = Project.objects.get_or_create_from_url(url)
        self.assertEqual(project.git_repository, url)
        self.assertTrue(project.approved)

    def test_get_project(self):
        url = 'git@github.com:tind/balder.git'
        Project.objects.get_or_create_from_url(url)
        self.assertEqual(Project.objects.all().count(), 1)
        Project.objects.get_or_create_from_url(url)
        self.assertEqual(Project.objects.all().count(), 1)

    @mock.patch('frigg.helpers.github.list_collaborators', lambda x: ['dumbledore'])
    def test_update_members(self):
        project = Project.objects.create(owner='frigg', name='frigg-worker', private=False)
        project.update_members()
        self.assertEqual(project.members.all().count(), 1)

    @override_settings(GITHUB_ACCESS_TOKEN='github-token')
    def test_token_for_url(self):
        self.assertEqual(Project.token_for_url('git@github.com:frigg/frigg.git'), 'github-token')

        project = Project.objects.get_or_create_from_url('git@github.com:frigg/frigg.git')
        project.user = get_user_model().objects.get(pk=1)
        project.save()
        social_auth = UserSocialAuth.objects.create(user=project.user, provider='github', uid='uid')
        social_auth.extra_data = {'access_token': 'user-token'}
        social_auth.save()
        self.assertEqual(Project.token_for_url('git@github.com:frigg/frigg.git'), 'user-token')


class BuildTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(owner='frigg', name='frigg-worker', approved=True)

    def tearDown(self):
        Project.objects.all().delete()
        Build.objects.all().delete()

    def test___str__(self):
        build = Build.objects.create(project=self.project, branch='master', build_number=1)
        self.assertEqual(str(build), 'frigg / frigg-worker / master')

    def test_queue_object(self):
        build = Build.objects.create(project=self.project, branch='master', sha='s', build_number=1)
        obj = build.queue_object
        self.assertEqual(obj['id'], build.pk)
        self.assertEqual(obj['branch'], build.branch)
        self.assertEqual(obj['sha'], build.sha)
        self.assertEqual(obj['clone_url'], build.project.clone_url)
        self.assertEqual(obj['owner'], build.project.owner)
        self.assertEqual(obj['name'], build.project.name)
        self.assertFalse('pull_request_id' in obj)
        build.pull_request_id = 42
        obj = build.queue_object
        self.assertEqual(obj['pull_request_id'], 42)

    def test_color(self):
        build = Build.objects.create(project=self.project, branch='master', build_number=1)
        self.assertEqual(build.color, 'orange')
        result = BuildResult.objects.create(build=build, succeeded=True)
        self.assertEqual(build.color, 'green')
        result.succeeded = False
        self.assertEqual(build.color, 'red')

    @responses.activate
    def test_send_webhook(self):
        responses.add(
            responses.POST,
            'http://w.frigg.io',
            body='Ok',
            content_type='application/json'
        )
        build = Build.objects.create(project=self.project, branch='master', build_number=1)
        BuildResult.objects.create(build=build, succeeded=True)
        response = build.send_webhook('http://w.frigg.io')
        request = json.loads(response.request.body)
        self.assertEqual(request['repository'], build.project.git_repository)
        self.assertEqual(request['sha'], build.sha)
        self.assertEqual(request['build_url'], build.get_absolute_url())
        self.assertEqual(request['state'], build.result.succeeded)
        self.assertEqual(request['return_code'], build.result.return_code)

    @mock.patch('frigg.helpers.github.set_commit_status')
    @mock.patch('redis.Redis', mock_redis_client)
    def test_start(self, mock_set_commit_status):
        build = Build.objects.create(project=self.project, branch='master', build_number=1)
        BuildResult.objects.create(build=build, succeeded=True)
        build.start()
        self.assertEqual(BuildResult.objects.all().count(), 0)
        self.assertTrue(mock_set_commit_status.called)

    @mock.patch('frigg.builds.models.BuildResult.create_not_approved')
    @mock.patch('redis.Redis', mock_redis_client)
    def test_start_not_approved(self, mock_create_not_approved):
        project = Project.objects.create(owner='tind', name='frigg', approved=False)
        build = Build.objects.create(project=project, branch='master', build_number=1)
        build.start()
        self.assertTrue(mock_create_not_approved.called)

    def test_has_timed_out(self):
        url = 'git@github.com:frigg/frigg.git'
        project = Project.objects.get_or_create_from_url(url)
        build = Build.objects.create(project=project, build_number=1,
                                     start_time=now() - timedelta(minutes=15))
        self.assertTrue(build.has_timed_out())
        build.start_time = now()
        self.assertFalse(build.has_timed_out())
        project.average_time = 120
        self.assertFalse(build.has_timed_out())
        build.start_time = now() - timedelta(seconds=60)
        self.assertFalse(build.has_timed_out())
        build.start_time = now() - timedelta(seconds=260)
        self.assertTrue(build.has_timed_out())

    def test_short_message(self):
        build = Build(
            project=self.project,
            branch='master',
            build_number=1,
            message='Multi\nLine\nMessage'
        )
        self.assertEqual(build.short_message, 'Multi')
        build = Build(
            project=self.project,
            branch='master',
            build_number=1,
            message='Single line message'
        )
        self.assertEqual(build.short_message, 'Single line message')


class BuildResultTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(owner='frigg', name='frigg-worker')
        self.build = Build.objects.create(project=self.project, branch='master', build_number=1)

    def tearDown(self):
        Project.objects.all().delete()
        Build.objects.all().delete()
        BuildResult.objects.all().delete()

    def test___str__(self):
        result = BuildResult.objects.create(build=self.build)
        self.assertEqual(str(result), 'frigg / frigg-worker / master - 1')

    def test_evaluate_results(self):
        self.assertTrue(BuildResult.evaluate_results([{'succeeded': True}]))
        self.assertTrue(BuildResult.evaluate_results([{'succeeded': True}, {}]))
        self.assertFalse(BuildResult.evaluate_results([{'succeeded': True}, {'succeeded': False}]))
        self.assertFalse(BuildResult.evaluate_results([{'succeeded': False}, {'succeeded': True}]))
        self.assertFalse(BuildResult.evaluate_results([{'succeeded': False}, {}]))

    def test_create_not_approved(self):
        result = BuildResult.create_not_approved(self.build)
        self.assertEqual(result.build_id, self.build.pk)
        self.assertFalse(result.succeeded)

    def test_tasks(self):
        result = BuildResult.objects.create(
            build=self.build,
            result_log=(
                BuildResult.create_log_string_for_task({'task': 'tox'}) +
                BuildResult.create_log_string_for_task({'task': 'tox', 'log': '{}'}) +
                BuildResult.create_log_string_for_task({
                    'task': 'tox',
                    'log': '{}',
                    'return_code': 0
                }) +
                BuildResult.create_log_string_for_task({
                    'task': 'tox',
                    'log': 'tested all the stuff\n1!"#$%&/()=?',
                    'return_code': 11
                }) +
                BuildResult.create_log_string_for_task({
                    'task': 'coverage report --fail-under=100'
                }) +
                BuildResult.create_log_string_for_task({
                    'task': 'tox',
                    'return_log': 'fail',
                    'return_code': 'd'
                })
            )
        )
        self.assertEqual(len(result.tasks), 5)
        self.assertEqual(result.tasks[0], ('tox', '\n', ''))
        self.assertEqual(result.tasks[1], ('tox', '{}\n', ''))
        self.assertEqual(result.tasks[2], ('tox', '{}\n', '0'))
        self.assertEqual(result.tasks[3], ('tox', 'tested all the stuff\n1!"#$%&/()=?\n', '11'))
        self.assertEqual(result.tasks[4], ('coverage report --fail-under=100', '\n', ''))

    def test_create_log_string_for_task(self):
        self.assertEqual(
            BuildResult.create_log_string_for_task({
                'task': 'tox',
                'log': 'tested all the stuff\n1!"#$%&/()=?',
                'return_code': 11
            }),
            (
                'Task: tox\n\n'
                '------------------------------------\n'
                'tested all the stuff\n1!"#$%&/()=?\n'
                '------------------------------------\n'
                'Exited with exit code: 11\n\n'
            )
        )

    def test_coverage_diff(self):
        start_time = datetime(2012, 12, 12, tzinfo=get_current_timezone())
        b1 = Build.objects.create(project=self.project, branch='i', build_number=4,
                                  start_time=start_time)
        positive_change = BuildResult.objects.create(build=b1, coverage=100)
        self.assertEqual(positive_change.coverage_diff, 100)

        master = Build.objects.create(project=self.project, branch='master', build_number=3,
                                      end_time=start_time - timedelta(hours=1))
        BuildResult.objects.create(build=master, coverage=20)

        # Need to fetch again to come around cached_property
        self.assertEqual(BuildResult.objects.get(pk=positive_change.pk).coverage_diff, 80)

        b2 = Build.objects.create(project=self.project, branch='i', build_number=5,
                                  start_time=start_time)
        negative_change = BuildResult.objects.create(build=b2, coverage=10)
        self.assertEqual(negative_change.coverage_diff, -10)

        b3 = Build.objects.create(project=self.project, branch='i', build_number=6,
                                  start_time=start_time)
        no_change = BuildResult.objects.create(build=b3, coverage=20)
        self.assertEqual(no_change.coverage_diff, 0)
