# -*- coding: utf8 -*-
from django.http import HttpResponse
from django.test import RequestFactory
from django.test.testcases import TestCase
from django.test.utils import override_settings
from frigg.authentication.decorators import worker_token_required


class DecoratorsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(FRIGG_WORKER_TOKENS=['token'])
    def test_worker_token_required(self):

        @worker_token_required
        def view(request):
            return HttpResponse(42)

        request = self.factory.get('/')
        response = view(request)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.content, b'')

        request = self.factory.get('/', HTTP_FRIGG_WORKER_TOKEN='token')
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'42')
