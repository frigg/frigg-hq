# -*- coding: utf8 -*-
import json
from unittest import skip
from decimal import Decimal

from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.test import TestCase, Client, RequestFactory, override_settings

from .api import report_build
from .models import BuildResult, Build


class BuildBadgeTestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml', 'frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def setUp(self):
        self.client = Client()
        with open(finders.find('badges/build-success.svg')) as f:
            self.success = bytes(f.read(), encoding='utf-8')
        with open(finders.find('badges/build-failure.svg')) as f:
            self.failure = bytes(f.read(), encoding='utf-8')

    def test_success(self):
        response = self.client.get(reverse('build_badge', args=['frigg', 'frigg']))
        self.assertStatusCode(response)
        self.assertEquals(response.content, self.success)

        response = self.client.get(reverse('build_badge',
                                           args=['frigg', 'frigg', 'another-branch']))
        self.assertStatusCode(response)
        self.assertEquals(response.content, self.success)

    def test_failure(self):
        BuildResult.objects.all().update(succeeded=False)
        response = self.client.get(reverse('build_badge', args=['frigg', 'frigg']))
        self.assertStatusCode(response)
        self.assertEquals(response.content, self.failure)

        response = self.client.get(reverse('build_badge',
                                           args=['frigg', 'frigg', 'another-branch']))
        self.assertStatusCode(response)
        self.assertEquals(response.content, self.failure)

    def test_404(self):
        response = self.client.get(reverse('build_badge', args=['frigg', 'nothing']))
        self.assertStatusCode(response, code=404)


class CoverageBadgeTestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml', 'frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def test_coverage(self):
        BuildResult.objects.all().update(coverage=92.5)
        response = self.client.get(reverse('coverage_badge', args=['frigg', 'frigg']))
        self.assertStatusCode(response)
        self.assertIsNotNone(response.content)
        self.assertContains(response, 'coverage')

        response = self.client.get(reverse('coverage_badge',
                                           args=['frigg', 'frigg', 'another-branch']))
        self.assertStatusCode(response)
        self.assertIsNotNone(response.content)
        self.assertContains(response, 'coverage')

    def test_404(self):
        response = self.client.get(reverse('coverage_badge', args=['frigg', 'nothing']))
        self.assertStatusCode(response, code=404)

    def test_unknown(self):
        response = self.client.get(reverse('coverage_badge', args=['frigg', 'frigg']))
        self.assertStatusCode(response)
        self.assertIsNotNone(response.content)
        self.assertContains(response, 'coverage')
        self.assertContains(response, 'unknown')


class APITestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml', 'frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def setUp(self):
        self.factory = RequestFactory()
        self.payload = {
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

    @skip('temporary turned off')
    def test_token_decorator(self):
        request = self.factory.post(reverse('worker_api_report_build'))
        response = report_build(request)
        self.assertStatusCode(response, 403)

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_report(self):
        request = self.factory.post(
            reverse('worker_api_report_build'),
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
        self.assertEquals(build.result.return_codes, [0])
        self.assertIsNone(build.result.coverage)
        self.assertEquals(
            build.result.result_log,
            'Task: make test\n\n------------------------------------\n'
            'log\n------------------------------------\nExited with exit code: 0\n\n'
            'Task: make test\n\n------------------------------------\n'
            '\n------------------------------------\nExited with exit code: \n\n'
        )

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_double_report(self):
        request = self.factory.post(
            reverse('worker_api_report_build'),
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
            reverse('worker_api_report_build'),
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
            reverse('worker_api_report_build'),
            data=json.dumps(self.payload),
            content_type='application/json',
            HTTP_FRIGG_WORKER_TOKEN='supertoken'
        )
        response = report_build(request)
        self.assertStatusCode(response, 404)
