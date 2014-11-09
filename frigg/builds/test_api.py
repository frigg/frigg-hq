# -*- coding: utf8 -*-
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.test import TestCase, Client

from frigg.builds.models import BuildResult


class BadgeTestCase(TestCase):
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
