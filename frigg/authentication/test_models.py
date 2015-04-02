# -*- coding: utf8 -*-
from unittest import mock

from django.test import TransactionTestCase
from social.apps.django_app.default.models import UserSocialAuth

from .models import User


class UserTestCase(TransactionTestCase):

    def tearDown(self):
        User.objects.all().delete()

    def test_github_token(self):
        user = User.objects.create_user('dumbledore')
        self.assertIsNone(user.github_token)
        social_auth = UserSocialAuth.objects.create(user=user, provider='github', uid='uid')
        social_auth.extra_data = {'access_token': 'user-token'}
        social_auth.save()
        self.assertEqual(User.objects.get(username='dumbledore').github_token, 'user-token')

    @mock.patch('frigg.helpers.github.update_repo_permissions')
    def test_update_repo_permissions(self, mock_update_repo_permissions):
        user = User.objects.create_user('dumbledore')
        user.github_token = 'token'
        user.update_repo_permissions()
        self.assertTrue(mock_update_repo_permissions.called)
