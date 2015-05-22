# -*- coding: utf8 -*-
from django.core.urlresolvers import reverse

from frigg.utils.tests import ViewTestCase

from .views import download_artifact


class BuildsViewTests(ViewTestCase):
    fixtures = ['frigg/builds/fixtures/users.json', 'frigg/builds/fixtures/test_views.yaml']

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
