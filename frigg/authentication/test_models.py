# -*- coding: utf8 -*-
from unittest import mock
from django.test import TestCase
from frigg.authentication.models import User


class UserTestCase(TestCase):

    def tearDown(self):
        User.objects.all().delete()

    def test_github_token(self):
        user = User.objects.create_user('dumbledore')
        self.assertIsNone(user.github_token)

    @mock.patch('frigg.helpers.github.update_repo_permissions')
    def test_update_repo_permissions(self, mock_update_repo_permissions):
        user = User.objects.create_user('dumbledore')
        user.github_token = 'token'
        user.update_repo_permissions()
        self.assertTrue(mock_update_repo_permissions.called)
