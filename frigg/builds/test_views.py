# -*- coding: utf8 -*-
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory

from .views import overview, view_build, view_organization, view_project


class SmokeTestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def setUp(self):
        self.user = get_user_model().objects.create(username='dumbledore')
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
