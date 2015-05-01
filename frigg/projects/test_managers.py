# -*- coding: utf8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TransactionTestCase

from .models import Project


class ProjectManagerTests(TransactionTestCase):
    fixtures = ['frigg/builds/fixtures/users.json',
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
