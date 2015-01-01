# -*- coding: utf8 -*-
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.http import Http404

from frigg.utils.tests import ViewTestCase
from .models import Project
from .views import (overview, view_build, view_organization, view_project, last_build,
                    approve_projects, download_artifact)


class SmokeTestCase(ViewTestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml', 'frigg/builds/fixtures/test_views.yaml']

    def tearDown(self):
        get_user_model().objects.all().delete()

    def test_overview_view(self):
        request = self.factory.get(reverse('overview'))
        self.add_request_fields(request)
        response = overview(request)
        self.assertStatusCode(response)

        self.add_request_fields(request, anonymous=True)
        response = overview(request)
        self.assertStatusCode(response)

    def test_overview_pagination(self):
        self.assertStatusCode(self.client.get(reverse('overview', args=[1])))
        self.assertStatusCode(self.client.get(reverse('overview', args=[10])), 404)

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

    def test_approve_projects_view(self):
        request = self.factory.get(reverse('approve_projects'))
        self.add_request_fields(request, superuser=True)
        response = approve_projects(request)
        self.assertStatusCode(response, 200)

    def test_approve_projects_post_view(self):
        Project.objects.create(pk=42)
        request = self.factory.post(reverse('approve_projects'), data={'id': 42})
        self.add_request_fields(request, superuser=True)
        response = approve_projects(request)
        self.assertStatusCode(response, 200)
        self.assertTrue(Project.objects.get(pk=42).approved)

    def test_download_artifact(self):
        request = self.factory.get(
            reverse('download_artifact', args=['frigg', 'frigg', 'htmlcov.zip'])
        )
        self.add_request_fields(request)
        response = download_artifact(request, 'frigg', 'frigg', 'htmlcov.zip')
        self.assertStatusCode(response, 200)
        self.assertEqual(response['X-Accel-Redirect'],
                         '/protected/artifacts/frigg/frigg/htmlcov.zip')
        self.assertEqual(response['Content-Disposition'],
                         'attachment; filename="htmlcov.zip"')

    def test_download_artifact_404(self):
        response = self.client.get(
            reverse('download_artifact', args=['frigg', 'non-existing', 'htmlcov.zip'])
        )
        self.assertStatusCode(response, 404)
