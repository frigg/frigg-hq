# -*- coding: utf8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from frigg.builds.models import BuildResult

from .models import Build, Project


class PermittedObjectsTestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml',
                'frigg/builds/fixtures/test_permitted_objects.yaml']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)

    def tearDown(self):
        get_user_model().objects.all().delete()
        Project.objects.all().delete()

    def test_project_permitted_objects(self):
        self.assertEqual(Project.objects.all().count(), 4)
        self.assertEqual(Project.objects.permitted(self.user).count(), 3)
        self.assertEqual(Project.objects.permitted(AnonymousUser()).count(), 2)

    def test_build_permitted_objects(self):
        self.assertEqual(Build.objects.all().count(), 5)
        self.assertEqual(Build.objects.permitted(self.user).count(), 4)
        self.assertEqual(Build.objects.permitted(AnonymousUser()).count(), 2)

    def test_build_result_permitted_objects(self):
        self.assertEqual(BuildResult.objects.all().count(), 5)
        self.assertEqual(BuildResult.objects.permitted(self.user).count(), 4)
        self.assertEqual(BuildResult.objects.permitted(AnonymousUser()).count(), 2)
