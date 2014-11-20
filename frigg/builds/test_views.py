# -*- coding: utf8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import TestCase, RequestFactory, Client
from frigg.builds.views import approve_projects

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

    def add_request_fields(self, request, anonymous=False):
        if anonymous:
            request.user = AnonymousUser()
        else:
            request.user = self.user

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_overview_view(self):
        request = self.factory.get(reverse('overview'))
        self.add_request_fields(request)
        response = overview(request)
        self.assertStatusCode(response)

        self.add_request_fields(request, anonymous=True)
        response = overview(request)
        self.assertStatusCode(response)

    def test_organization_view(self):
        request = self.factory.get(reverse('view_organization', args=['frigg']))
        self.add_request_fields(request)
        response = view_organization(request, 'frigg')
        self.assertStatusCode(response)

        request = self.factory.get(reverse('view_organization', args=['dumbledore']))
        self.add_request_fields(request)
        self.assertRaises(Http404, view_organization, request, 'dumbledore')

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

        request = self.factory.get(reverse('last_build', args=['frigg', 'chewie']))
        self.add_request_fields(request, anonymous=True)
        self.assertRaises(Http404, last_build, request, 'frigg', 'chewie')

    def test_approve_project_404(self):
        response = self.client.get(reverse('approve_projects'))
        self.assertStatusCode(response, 404)

        response = self.client.get(reverse('approve_project', args=[1]))
        self.assertStatusCode(response, 404)

    def test_approve_projects_view(self):
        request = self.factory.get(reverse('approve_projects'))
        self.add_request_fields(request)
        response = approve_projects(request)
        self.assertStatusCode(response, 200)
