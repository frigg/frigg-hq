# -*- coding: utf8 -*-
import json
from decimal import Decimal
from unittest import skip

from django.core.urlresolvers import reverse
from django.test import RequestFactory, TransactionTestCase, override_settings

from .api import report_build
from .models import Build


class APITestCase(TransactionTestCase):
    fixtures = ['frigg/builds/fixtures/users.json', 'frigg/builds/fixtures/test_views.yaml']

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
        self.assertFalse(build.result.still_running)
        self.assertIsNone(build.result.coverage)
        self.assertEquals(
            json.loads(build.result.result_log),
            self.payload['results']
        )

    @override_settings(FRIGG_WORKER_TOKENS=['supertoken'])
    def test_report_pending(self):
        self.payload['finished'] = False
        self.payload['results'].append({'task': 'flake8', 'pending': True})
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
        self.assertTrue(build.result.still_running)
        self.assertIsNone(build.result.coverage)
        self.assertEquals(
            json.loads(build.result.result_log),
            self.payload['results']
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
