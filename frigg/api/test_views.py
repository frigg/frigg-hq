# -*- coding: utf-8 -*-
import json

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from frigg.builds.models import Build, BuildResult, Project


class APITestMixin(object):
    def assertProject(self, obj, project_id):
        project = Project.objects.get(pk=project_id)
        self.assertEqual(obj['id'], project.id)
        self.assertEqual(obj['owner'], project.owner)
        self.assertEqual(obj['name'], project.name)
        self.assertEqual(obj['private'], project.private)
        self.assertEqual(obj['approved'], project.approved)

    def assertBuild(self, obj, build_id):
        build = Build.objects.get(pk=build_id)
        self.assertEqual(obj['id'], build.pk)
        self.assertEqual(obj['sha'], build.sha)
        self.assertEqual(obj['branch'], build.branch)
        self.assertProject(obj['project'], build.project_id)
        self.assertBuildResult(obj['result'], build.result.pk)

    def assertBuildResult(self, obj, build_result_id):
        result = BuildResult.objects.get(pk=build_result_id)
        self.assertEqual(obj['id'], result.id)
        self.assertEqual(obj['coverage'], result.coverage)
        self.assertEqual(obj['succeeded'], result.succeeded)
        self.assertEqual(obj['tasks'], result.tasks)

    def assertNotAllowed(self, method, url):
        response = getattr(self.client, method)(url)
        self.assertEqual(response.status_code, 403)


class ProjectAPITestCase(APITestCase, APITestMixin):
    fixtures = ['frigg/builds/fixtures/users.yaml', 'frigg/api/fixtures/test_views.yaml']

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.get(pk=1)

    def tearDown(self):
        Project.objects.all().delete()

    def test_get_projects_anonymous(self):
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode())
        self.assertEqual(len(json_response), 2)
        self.assertProject(json_response[0], 3)
        self.assertProject(json_response[1], 4)

    def test_get_projects_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/projects/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode())
        self.assertEqual(len(json_response), 3)
        self.assertProject(json_response[0], 1)
        self.assertProject(json_response[1], 3)
        self.assertProject(json_response[2], 4)
        response = self.client.get('/api/projects/2/')
        self.assertEqual(response.status_code, 404)

    def test_get_project_anonymous(self):
        response = self.client.get('/api/projects/4/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode())
        self.assertProject(json_response, 4)
        response = self.client.get('/api/projects/1/')
        self.assertEqual(response.status_code, 404)

    def test_get_project_authenticated(self):
        response = self.client.get('/api/projects/4/')
        self.assertEqual(response.status_code, 200)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/projects/1/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode())
        self.assertProject(json_response, 1)

    def test_get_project_404(self):
        response = self.client.get('/api/projects/1/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/api/projects/300/')
        self.assertEqual(response.status_code, 404)

    def test_post_not_allowed(self):
        self.assertNotAllowed('post', '/api/projects/2/')

        self.client.force_authenticate(user=self.user)
        self.assertNotAllowed('post', '/api/projects/2/')


class BuildAPITestCase(APITestCase, APITestMixin):
    fixtures = ['frigg/builds/fixtures/users.yaml', 'frigg/api/fixtures/test_views.yaml']

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.get(pk=1)

    def tearDown(self):
        Project.objects.all().delete()

    def test_get_builds_anonymous(self):
        response = self.client.get('/api/builds/')
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response['count'], 2)
        self.assertBuild(json_response['results'][0], 5)
        self.assertBuild(json_response['results'][1], 4)

    def test_get_builds_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/builds/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode())
        self.assertEqual(json_response['count'], 4)
        self.assertBuild(json_response['results'][0], 5)
        self.assertBuild(json_response['results'][1], 4)
        self.assertBuild(json_response['results'][2], 2)
        self.assertBuild(json_response['results'][3], 1)

    def test_get_build_anonymous(self):
        response = self.client.get('/api/builds/5/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode())
        self.assertBuild(json_response, 5)
        response = self.client.get('/api/builds/1/')
        self.assertEqual(response.status_code, 404)

    def test_get_build_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/builds/1/')
        self.assertEqual(response.status_code, 200)
        json_response = json.loads(response.content.decode())
        self.assertBuild(json_response, 1)

    def test_get_build_404(self):
        response = self.client.get('/api/builds/3/')
        self.assertEqual(response.status_code, 404)

        response = self.client.get('/api/builds/300/')
        self.assertEqual(response.status_code, 404)

    def test_post_not_allowed(self):
        self.assertNotAllowed('post', '/api/builds/1/')

        self.client.force_authenticate(user=self.user)
        self.assertNotAllowed('post', '/api/builds/1/')
