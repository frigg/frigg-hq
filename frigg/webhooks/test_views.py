# -*- coding: utf8 -*-
import json
from unittest import mock
from django.contrib.auth import get_user_model

from django.core.urlresolvers import reverse

from frigg.utils.tests import ViewTestCase
from frigg.builds.models import Project


@mock.patch('frigg.builds.models.Build.start', lambda x: x)
class GithubWebhookTestCase(ViewTestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml']

    def post_webhook(self, event, data={}):
        return self.client.post(
            reverse('webhooks:github'),
            json.dumps(data),
            content_type='application/json',
            HTTP_X_GITHUB_EVENT=event
        )

    def tearDown(self):
        Project.objects.all().delete()

    def test_no_event(self):
        response = self.client.post(reverse('webhooks:github'))
        self.assertEqual(response.content.decode('UTF-8'), 'Missing HTTP_X_GITHUB_EVENT')

    def test_unknown_event(self):
        response = self.post_webhook('superevent')
        self.assertEqual(response.content.decode('UTF-8'), 'Unknown event: superevent')

    @mock.patch('frigg.helpers.github.parse_ping_payload',
                lambda x: GithubWebhookTestCase.ping_data)
    @mock.patch('frigg.helpers.github.list_collaborators', lambda x: ['dumbledore'])
    def test_ping_handling(self):
        response = self.post_webhook('ping')
        self.assertStatusCode(response)
        self.assertContains(response, 'Added project frigg / frigg-worker')
        self.assertIsNotNone(Project.objects.get(owner='frigg', name='frigg-worker', private=False))

    @mock.patch('frigg.helpers.github.parse_ping_payload',
                lambda x: GithubWebhookTestCase.ping_data_user)
    @mock.patch('frigg.helpers.github.list_collaborators', lambda x: ['dumbledore'])
    def test_ping_handling_of_user_repo(self):
        response = self.post_webhook('ping')
        self.assertStatusCode(response)
        self.assertContains(response, 'Added project dumbledore / da')
        self.assertIsNotNone(Project.objects.get(owner='dumbledore', name='da', private=False))

    @mock.patch('frigg.helpers.github.parse_push_payload',
                lambda x: GithubWebhookTestCase.push_data)
    def test_push_handling(self):
        response = self.post_webhook('push', {'ref': 'refs/heads/master'})
        self.assertStatusCode(response)
        self.assertIsNotNone(Project.objects.get(owner='frigg', name='frigg-worker', private=False))

    @mock.patch('frigg.helpers.github.parse_push_payload', lambda x: None)
    def test_push_not_master_handling(self):
        response = self.post_webhook('push', {'ref': 'refs/heads/other-branch'})
        self.assertStatusCode(response)
        self.assertContains(response, 'Could not handle event')

    @mock.patch('frigg.helpers.github.parse_pull_request_payload',
                lambda x: GithubWebhookTestCase.pull_request_data)
    def test_pull_request_handling(self):
        response = self.post_webhook('pull_request')
        self.assertStatusCode(response)
        self.assertIsNotNone(Project.objects.get(owner='frigg', name='frigg-worker', private=False))

    @mock.patch('frigg.helpers.github.parse_comment_payload',
                lambda x: GithubWebhookTestCase.issue_comment_data)
    def test_issue_comment_handling(self):
        response = self.post_webhook('issue_comment')
        self.assertStatusCode(response)
        self.assertIsNotNone(Project.objects.get(owner='frigg', name='frigg-worker', private=False))

    @mock.patch('frigg.helpers.github.parse_member_payload',
                lambda x: GithubWebhookTestCase.member_data)
    def test_member_handling(self):
        response = self.post_webhook('member', {'action': 'nothing'})
        self.assertStatusCode(response)
        self.assertContains(response, 'Unknown action')

        Project.objects.create(owner='frigg', name='frigg-worker')
        response = self.post_webhook('member', {
            'action': 'added',
            'member': {'login': 'dumbledore'}
        })
        self.assertStatusCode(response)
        self.assertContains(response, 'Added dumbledore to the project')
        self.assertIsNotNone(Project.objects.get(name='frigg-worker',
                                                 members__username='dumbledore'))

    @mock.patch('frigg.helpers.github.parse_member_payload',
                lambda x: GithubWebhookTestCase.member_data)
    def test_member_handling_of_unknown_user(self):
        get_user_model().objects.all().delete()
        response = self.post_webhook('member', {
            'action': 'added',
            'member': {'login': 'dumbledore'}
        })
        self.assertStatusCode(response)
        self.assertContains(response, 'Unknown user dumbledore')

    ping_data = {
        'repo_url': 'git@github.com:frigg/frigg-worker.git',
        'repo_name': 'frigg-worker',
        'repo_owner': 'frigg',
        'private': False,
    }

    ping_data_user = {
        'repo_url': 'git@github.com:dumbledore/da.git',
        'repo_name': 'da',
        'repo_owner': 'dumbledore',
        'private': False,
    }

    push_data = {
        'repo_url': 'git@github.com:frigg/frigg-worker.git',
        'repo_name': 'frigg-worker',
        'repo_owner': 'frigg',
        'private': False,
        'pull_request_id': 0,
        'branch': 'master',
        'sha': 'hash that stuff'
    }

    pull_request_data = {
        'repo_url': 'git@github.com:frigg/frigg-worker.git',
        'repo_name': 'frigg-worker',
        'repo_owner': 'frigg',
        'private': False,
        'pull_request_id': 1,
        'branch': 'patch-1',
        'sha': 'hash that stuff'
    }

    issue_comment_data = {
        'repo_url': 'git@github.com:frigg/frigg-worker.git',
        'repo_name': 'frigg-worker',
        'repo_owner': 'frigg',
        'private': False,
        'pull_request_id': 1,
        'branch': 'pull-request',
        'sha': 'hash that stuff'
    }

    member_data = {
        'repo_url': 'git@github.com:frigg/frigg-worker.git',
        'repo_name': 'frigg-worker',
        'repo_owner': 'frigg',
        'action': 'added',
        'username': 'dumbledore'
    }
