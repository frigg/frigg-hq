# -*- coding: utf8 -*-
from django.test import TestCase

from .models import Project, BuildResult


class ProjectTestCase(TestCase):
    def tearDown(self):
        Project.objects.all().delete()

    def test_create_project(self):
        url = 'git@github.com:tind/balder.git'
        project = Project.objects.get_or_create_from_url(url)
        self.assertEqual(project.owner, 'tind')
        self.assertEqual(project.name, 'balder')
        self.assertEqual(project.git_repository, url)
        self.assertIsNone(project.average_time)
        self.assertFalse(project.approved)
        self.assertEqual(Project.objects.all().count(), 1)

    def test_auto_approval(self):
        url = 'git@github.com:frigg/frigg.git'
        project = Project.objects.get_or_create_from_url(url)
        self.assertEqual(project.git_repository, url)
        self.assertTrue(project.approved)

    def test_get_project(self):
        url = 'git@github.com:tind/balder.git'
        Project.objects.get_or_create_from_url(url)
        self.assertEqual(Project.objects.all().count(), 1)
        Project.objects.get_or_create_from_url(url)
        self.assertEqual(Project.objects.all().count(), 1)


class BuildResultTestCase(TestCase):

    def test_evaluate_results(self):
        self.assertTrue(BuildResult.evaluate_results([{'succeeded': True}]))
        self.assertTrue(BuildResult.evaluate_results([{'succeeded': True}, {}]))
        self.assertFalse(BuildResult.evaluate_results([{'succeeded': True}, {'succeeded': False}]))
        self.assertFalse(BuildResult.evaluate_results([{'succeeded': False}, {'succeeded': True}]))
        self.assertFalse(BuildResult.evaluate_results([{'succeeded': False}, {}]))
