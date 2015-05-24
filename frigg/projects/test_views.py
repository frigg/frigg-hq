# -*- coding: utf8 -*-
from django.contrib.staticfiles import finders
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import TestCase

from frigg.builds.models import BuildResult
from frigg.utils.tests import ViewTestCase

from .models import Project
from .views import approve_projects, view_organization, view_project


class ProjectViewTests(ViewTestCase):
    fixtures = ['frigg/builds/fixtures/users.json', 'frigg/builds/fixtures/test_views.yaml']

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

    def test_approve_project_404(self):
        response = self.client.get(reverse('approve_projects_overview'))
        self.assertStatusCode(response, 404)

    def test_approve_projects_view(self):
        request = self.factory.get(reverse('approve_projects_overview'))
        self.add_request_fields(request, superuser=True)
        response = approve_projects(request)
        self.assertStatusCode(response, 200)

    def test_approve_projects_post_view(self):
        Project.objects.create(pk=42)
        request = self.factory.post(reverse('approve_project', args=[42]), data={'approve': 'yes'})
        self.add_request_fields(request, superuser=True)
        response = approve_projects(request, project_id=42)
        self.assertStatusCode(response, 302)
        self.assertTrue(Project.objects.get(pk=42).approved)

    def test_approve_projects_triggers_build_last(self):
        project = Project.objects.get(pk=2)
        last_build_start_time = project.builds.last().start_time
        self.assertIsNone(last_build_start_time)

        request = self.factory.post(reverse('approve_project', args=[1]), data={'approve': 'yes'})
        self.add_request_fields(request, superuser=True)
        approve_projects(request, project_id=2)

        self.assertNotEqual(last_build_start_time, project.builds.last().start_time)


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
