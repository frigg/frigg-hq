# -*- coding: utf8 -*-
import json
from unittest import skip

from django.contrib.auth import get_user_model
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.test.utils import override_settings

from .api import report_build
from .models import Build
from .views import overview, view_build, view_organization, view_project, last_build


class SmokeTestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml', 'frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.factory = RequestFactory()

    def tearDown(self):
        get_user_model().objects.all().delete()

    def add_request_fields(self, request):
        request.user = self.user
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_overview_view(self):
        request = self.factory.get(reverse('overview'))
        self.add_request_fields(request)
        response = overview(request)
        self.assertStatusCode(response)

    def test_organization_view(self):
        request = self.factory.get(reverse('view_organization', args=['tind']))
        self.add_request_fields(request)
        response = view_organization(request, 'frigg')
        self.assertStatusCode(response)

    def test_project_view(self):
        request = self.factory.get(reverse('view_project', args=['frigg', 'frigg']))
        self.add_request_fields(request)
        response = view_project(request, 'frigg', 'frigg')
        self.assertStatusCode(response)

    def test_build_view(self):
        request = self.factory.get(reverse('view_build', args=['frigg', 'frigg', 1]))
        self.add_request_fields(request)
        response = view_build(request, 'frigg', 'frigg', '1')
        self.assertStatusCode(response)

    def test_last_build_view(self):
        request = self.factory.get(reverse('last_build', args=['frigg', 'frigg']))
        self.add_request_fields(request)
        response = last_build(request, 'frigg', 'frigg')
        self.assertStatusCode(response, 302)
        self.assertTrue(response.url.endswith(reverse('view_build', args=['frigg', 'frigg', 3])))


class APITestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml', 'frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def setUp(self):
        self.factory = RequestFactory()

    @skip('temporary turned off')
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
        build = Build.objects.get(pk=2)
        self.assertFalse(build.is_pending)
        self.assertTrue(build.result.succeeded)
        self.assertEquals(build.result.return_codes, [0])
        self.assertEquals(
            build.result.result_log,
            'Task: make test\n\n------------------------------------\n'
            'log\n------------------------------------\nExited with exit code: 0\n\n'
            'Task: make test\n\n------------------------------------\n'
            '\n------------------------------------\nExited with exit code: \n\n'
        )
