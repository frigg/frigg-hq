# -*- coding: utf8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404

from frigg.utils.tests import ViewTestCase

from .views import download_artifact, last_build, overview, view_build


class BuildsViewTests(ViewTestCase):
    fixtures = ['frigg/builds/fixtures/users.json', 'frigg/builds/fixtures/test_views.yaml']

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
        response = self.client.get(reverse('approve_projects_overview'))
        self.assertStatusCode(response, 404)

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
