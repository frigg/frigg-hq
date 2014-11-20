# -*- coding: utf8 -*-
from unittest import mock

from django.test import TestCase

from .models import Project, BuildResult, Build


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


class BuildTestCase(TestCase):
    def setUp(self):
        self.project = Project.objects.create(owner='frigg', name='frigg-worker')

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
