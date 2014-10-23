# -*- coding: utf8 -*-
import json
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

from .api import report_build
from frigg.builds.models import BuildResult
from .views import overview, view_build, view_organization, view_project


class SmokeTestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml', 'frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.factory = RequestFactory()

    def tearDown(self):
        get_user_model().objects.all().delete()

    def test_overview_view(self):
        request = self.factory.get(reverse('overview'))
        request.user = self.user
        response = overview(request)
        self.assertStatusCode(response)

    def test_organization_view(self):
        request = self.factory.get(reverse('view_organization', args=['tind']))
        request.user = self.user
        response = view_organization(request, 'tind')
        self.assertStatusCode(response)

    def test_project_view(self):
        request = self.factory.get(reverse('view_project', args=['tind', 'frigg']))
        request.user = self.user
        response = view_project(request, 'tind', 'frigg')
        self.assertStatusCode(response)

    def test_build_view(self):
        request = self.factory.get(reverse('view_build', args=['tind', 'frigg', 1]))
        request.user = self.user
        response = view_build(request, 'tind', 'frigg', '1')
        self.assertStatusCode(response)


class APITestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml', 'frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def setUp(self):
        self.factory = RequestFactory()

    def test_token_decorator(self):
        request = self.factory.post(reverse('worker_api_report_build'))
        response = report_build(request)
        self.assertStatusCode(response, 403)

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_report(self):
        payload = {
            "sha": "superbhash",
            "clone_url": "https://github.com/frigg/frigg-worker.git",
            "name": "frigg-worker",
            "branch": "master",
            "owner": "frigg",
            "id": 2,
            "results": [
                {"task": "make test", "return_code": 0, "succeeded": True, "log": "log"},
                {"task": "make test"}
            ]
        }
        request = self.factory.post(
            reverse('worker_api_report_build'),
            data=json.dumps(payload),
            content_type='application/json',
            HTTP_FRIGG_WORKER_TOKEN='supertoken'
        )
        response = report_build(request)
        self.assertStatusCode(response)
        self.assertContains(response, 'Thanks for building it')
