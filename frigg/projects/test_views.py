from unittest import skip

from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.test import TestCase

from frigg.builds.models import BuildResult


class BuildBadgeViewTests(TestCase):
    fixtures = ['frigg/builds/fixtures/users.json', 'frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def setUp(self):
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


class CoverageBadgeViewTests(TestCase):
    fixtures = ['frigg/builds/fixtures/users.json', 'frigg/builds/fixtures/test_views.yaml']

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    @skip("service is down")
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
