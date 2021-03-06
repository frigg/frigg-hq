from django.core.urlresolvers import reverse
from django.http import Http404

from frigg.builds.views import download_artifact, last_build
from frigg.utils.tests import ViewTestCase


class BuildsViewTests(ViewTestCase):
    fixtures = ['frigg/builds/fixtures/users.json', 'frigg/builds/fixtures/test_views.yaml']

    def test_last_build_view(self):
        request = self.factory.get(reverse('last_build', args=['frigg', 'frigg']))
        self.add_request_fields(request)
        response = last_build(request, 'frigg', 'frigg')
        self.assertStatusCode(response, 302)
        self.assertTrue(response.url.endswith('frigg/frigg/3'))

        request = self.factory.get(reverse('last_build', args=['frigg', 'chewie']))
        self.add_request_fields(request, anonymous=True)
        self.assertRaises(Http404, last_build, request, 'frigg', 'chewie')

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
