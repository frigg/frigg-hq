# -*- coding: utf-8 -*-
import json
from decimal import Decimal
from unittest import skip

from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import RequestFactory, TestCase, override_settings
from rest_framework.test import APIClient, APITestCase

from frigg.api.views import report_build, report_deployment
from frigg.authentication.models import User
from frigg.builds.models import Build, BuildResult, Project
from frigg.deployments.models import PRDeployment


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
        self.assertEqual(obj['setup_tasks'], result.setup_tasks)
        self.assertEqual(obj['service_tasks'], result.service_tasks)

    def assertNotAllowed(self, method, url):
        response = getattr(self.client, method)(url)
        self.assertEqual(response.status_code, 403)


class ProjectAPITestCase(APITestCase, APITestMixin):
    fixtures = ['frigg/builds/fixtures/users.json', 'frigg/api/fixtures/test_views.yaml']

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
    fixtures = ['frigg/builds/fixtures/users.json', 'frigg/api/fixtures/test_views.yaml']

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

    def test_get_build_by_owner_name_build_number_404(self):
        response = self.client.get('/api/builds/frigg/frigg/1/')
        self.assertEqual(response.status_code, 404)

    def test_build_id_same_as_build_by_owner_name_build_number(self):
        response_by_id = self.client.get('/api/builds/5/')
        self.assertEqual(response_by_id.status_code, 200)

        response_by_owner_name_build_number = self.client.get('/api/builds/frigg/frigg-worker/1/')
        self.assertEqual(response_by_owner_name_build_number.status_code, 200)

        self.assertEqual(response_by_id.content, response_by_owner_name_build_number.content)

    def test_get_builds_by_owner_name_404(self):
        response = self.client.get('/api/builds/frigg/frigg-hq/')
        self.assertEqual(response.status_code, 404)

    def test_get_builds_by_owner_name(self):
        response = self.client.get('/api/builds/frigg/frigg-worker/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content.decode())), 1)

    def test_get_builds_by_owner_404(self):
        response = self.client.get('/api/builds/beaver/')
        self.assertEqual(response.status_code, 404)

    def test_get_builds_by_owner(self):
        response = self.client.get('/api/builds/frigg/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content.decode())), 2)


class UserAPITests(TestCase):
    fixtures = ['frigg/builds/fixtures/users.json']

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.first()

    def test_me_api_view_anonymous(self):
        response = self.client.get(reverse('api:user_me'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertTrue(data['is_anonymous'], 'User is not anonymous')
        self.assertFalse(data['is_staff'], 'Anonymous user is staff')

    def test_me_api_view(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('api:user_me'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode())
        self.assertFalse(data['is_anonymous'], 'User is anonymous')
        self.assertEqual(data['username'], 'dumbledore')
        self.assertEqual(data['email'], 'albus@hogwarts.com')
        self.assertTrue(data['is_staff'], 'Dumbledore is not staff')

    def test_me_api_view_not_staff(self):
        self.user.is_staff = False
        self.user.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('api:user_me'))
        data = json.loads(response.content.decode())
        self.assertFalse(data['is_staff'], 'Dumbledore is staff')


class ReportBuildAPITests(APITestCase):
    fixtures = ['frigg/builds/fixtures/users.json', 'frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('api:worker_api_report_build')
        self.payload = {
            "sha": "superbhash",
            "clone_url": "https://github.com/frigg/frigg-worker.git",
            "name": "frigg-worker",
            "branch": "master",
            "owner": "frigg",
            "id": 2,
            "service_results": [
                {"task": "service redis-server start", "return_code": 0, "succeeded": True,
                 "log": "setup done"},
            ],
            "setup_results": [
                {"task": "make install", "return_code": 0, "succeeded": True, "log": "setup done"},
            ],
            "results": [
                {"task": "make test", "return_code": 0, "succeeded": True, "log": "log"},
                {"task": "make test"}
            ]
        }

    @skip('temporary turned off')
    def test_token_decorator(self):
        request = self.factory.post(self.url)
        response = report_build(request)
        self.assertStatusCode(response, 403)

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_report(self):
        request = self.factory.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_FRIGG_WORKER_TOKEN='supertoken'
        )
        response = report_build(request)
        self.assertStatusCode(response)
        self.assertContains(response, 'Thanks for building it')
        build = Build.objects.get(pk=2)
        self.assertFalse(build.is_pending)
        self.assertTrue(build.result.succeeded)
        self.assertFalse(build.result.still_running)
        self.assertIsNone(build.result.coverage)
        self.assertEquals(
            json.loads(build.result.result_log),
            self.payload['results']
        )
        self.assertEquals(
            json.loads(build.result.setup_log),
            self.payload['setup_results']
        )
        self.assertEquals(
            json.loads(build.result.service_log),
            self.payload['service_results']
        )

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_report_pending(self):
        self.payload['finished'] = False
        self.payload['results'].append({'task': 'flake8', 'pending': True})
        request = self.factory.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_FRIGG_WORKER_TOKEN='supertoken'
        )
        response = report_build(request)
        self.assertStatusCode(response)
        self.assertContains(response, 'Thanks for building it')
        build = Build.objects.get(pk=2)
        self.assertFalse(build.is_pending)
        self.assertTrue(build.result.succeeded)
        self.assertTrue(build.result.still_running)
        self.assertIsNone(build.result.coverage)
        self.assertEquals(
            json.loads(build.result.result_log),
            self.payload['results']
        )

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_double_report(self):
        request = self.factory.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_FRIGG_WORKER_TOKEN='supertoken'
        )
        response = report_build(request)
        self.assertStatusCode(response)
        response = report_build(request)
        self.assertStatusCode(response)

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_coverage(self):
        self.payload['coverage'] = 99.9
        request = self.factory.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_FRIGG_WORKER_TOKEN='supertoken'
        )
        response = report_build(request)
        self.assertStatusCode(response)
        build = Build.objects.get(pk=2)
        self.assertEqual(build.result.coverage, Decimal('99.9'))

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_404_report(self):
        self.payload['id'] = 200
        request = self.factory.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_FRIGG_WORKER_TOKEN='supertoken'
        )
        response = report_build(request)
        self.assertStatusCode(response, 404)


class ReportDeploymentAPITests(APITestCase):
    fixtures = ['frigg/builds/fixtures/users.json', 'frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def setUp(self):
        self.factory = RequestFactory()
        self.deployment = PRDeployment.objects.create(build_id=2, port=4000)
        self.url = reverse('api:worker_api_report_deployment')
        self.view = report_deployment
        self.payload = {
            'id': self.deployment.pk,
            'results': [{'task': 'make deploy', 'return_code': 0, 'succeeded': True, 'log': 'log'}]
        }

    @skip('temporary turned off')
    def test_token_decorator(self):
        request = self.factory.post(self.url)
        response = self.view(request)
        self.assertStatusCode(response, 403)

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_report(self):
        request = self.factory.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_FRIGG_WORKER_TOKEN='supertoken'
        )
        response = self.view(request)
        self.assertStatusCode(response)
        self.assertContains(response, 'Thanks for deploying it')
        deployment = PRDeployment.objects.get(pk=self.deployment.pk)
        self.assertTrue(deployment.succeeded)
        self.assertEqual(
            deployment.tasks,
            [{"task": "make deploy", "succeeded": True, "return_code": 0, "log": "log"}]
        )

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_double_report(self):
        request = self.factory.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_FRIGG_WORKER_TOKEN='supertoken'
        )
        response = self.view(request)
        self.assertStatusCode(response)
        response = self.view(request)
        self.assertStatusCode(response)

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_404_report(self):
        self.payload['id'] = 200
        request = self.factory.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_FRIGG_WORKER_TOKEN='supertoken'
        )
        response = self.view(request)
        self.assertStatusCode(response, 404)
