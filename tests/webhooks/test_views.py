# -*- coding: utf8 -*-
import json
import os
from unittest import mock

from django.conf import settings
from django.core.urlresolvers import reverse

from frigg.builds.models import Build, Project
from frigg.utils.tests import ViewTestCase


class WebhookViewTestCase(ViewTestCase):
    fixtures = ['frigg/builds/fixtures/users.json']
    FIXTURE_PATH = ''

    def load_fixture(self, fixture):
        fixtures_path = os.path.join(settings.BASE_DIR, self.FIXTURE_PATH, fixture)
        return json.load(open(fixtures_path, encoding='utf-8'))

    def get_webhook_headers(self, event, data=None, fixture=None):
        return {}

    def post_webhook(self, event, data=None, fixture=None):
        if not data and fixture:
            data = self.load_fixture(fixture)

        return self.client.post(
            reverse('webhooks:github'),
            json.dumps(data),
            content_type='application/json',
            **self.get_webhook_headers(event, data, fixture)
        )


@mock.patch('frigg.builds.models.Project.start_build')
class GithubWebhookViewTests(WebhookViewTestCase):
    FIXTURE_PATH = 'webhooks/fixtures/github'

    def get_webhook_headers(self, event, data=None, fixture=None):
        return {'HTTP_X_GITHUB_EVENT': event}

    def test_no_event(self, mock_start_build):
        response = self.client.post(reverse('webhooks:github'))
        self.assertEqual(response.content.decode('UTF-8'), 'Missing HTTP_X_GITHUB_EVENT')
        self.assertFalse(mock_start_build.called)

    def test_unknown_event(self, mock_start_build):
        response = self.post_webhook('superevent')
        self.assertEqual(response.content.decode('UTF-8'), 'Unknown event type "superevent"')
        self.assertFalse(mock_start_build.called)

    @mock.patch('frigg.helpers.github.list_collaborators', lambda x: ['dumbledore'])
    def test_ping_handling(self, mock_start_build):
        response = self.post_webhook('ping', fixture='ping.json')
        self.assertStatusCode(response)
        self.assertEqual(
            Project.objects.filter(owner='frigg', name='frigg', private=False).count(),
            1
        )
        self.assertFalse(mock_start_build.called)

    def test_ping_handling_of_organization_ping(self, mock_start_build):
        response = self.post_webhook('ping', fixture='ping_organization.json')
        self.assertStatusCode(response)
        self.assertContains(response, 'Handled "ping"')
        self.assertFalse(mock_start_build.called)

    def test_push_handling(self, mock_start_build):
        response = self.post_webhook('push', fixture='push_master.json')
        self.assertStatusCode(response)
        self.assertEqual(
            Project.objects.filter(owner='tind', name='frigg', private=False).count(),
            1
        )
        mock_start_build.assert_called_once_with({
            'pull_request_id': 0,
            'author': 'frecar',
            'sha': 'fddd2887efd63196e48fd5d6bc0e62e1bafa0276',
            'branch': 'master',
            'message': 'Rebased master, cleaned up imports'
        })

    def test_force_push_handling(self, mock_start_build):
        response = self.post_webhook('push', fixture='push_force.json')
        self.assertStatusCode(response)
        self.assertEqual(
            Project.objects.filter(owner='frigg', name='frigg', private=False).count(),
            1
        )
        mock_start_build.assert_called_once_with({
            'pull_request_id': 0,
            'author': 'frecar',
            'sha': '8dcab86e80470f8e3d3ee2f8cbdb9f7d3591b319',
            'branch': 'frecar/frigg-services',
            'message': 'Adds services in .frigg.yml'
        })

    def test_branch_push_handling(self, mock_start_build):
        response = self.post_webhook('push', fixture='push_branch.json')
        self.assertStatusCode(response)
        self.assertEqual(
            Project.objects.filter(owner='tind', name='frigg', private=False).count(),
            1
        )
        mock_start_build.assert_called_once_with({
            'pull_request_id': 0,
            'author': 'frecar',
            'sha': 'fddd2887efd63196e48fd5d6bc0e62e1bafa0276',
            'branch': 'branch',
            'message': 'Rebased master, cleaned up imports'
        })

    def test_tag_push_handling(self, mock_start_build):
        response = self.post_webhook('push', fixture='push_tag.json')
        self.assertStatusCode(response)
        self.assertEqual(
            Project.objects.filter(owner='relekang', name='python-thumbnails').count(),
            1
        )
        mock_start_build.assert_called_once_with({
            'pull_request_id': 0,
            'author': 'relekang',
            'sha': '7e037cbb6d7f923592671d07542b21c18373f886',
            'branch': '0.5.1',
            'message': '0.5.1'
        })

    def test_push_delete(self, mock_start_build):
        response = self.post_webhook('push', fixture='push_delete.json')
        self.assertStatusCode(response)
        self.assertFalse(mock_start_build.called)

    def test_push_delete_mark_builds_as_not_succeeded(self, mock_start_build):
        project = Project.objects.get_or_create(owner='frigg', name='frigg-hq', private=False)[0]
        Build.objects.get_or_create(
            project=project,
            branch="frecar/add-worker-host"
        )

        response = self.post_webhook('delete', fixture='push_delete_branch.json')
        self.assertStatusCode(response)
        self.assertFalse(mock_start_build.called)

        project = Project.objects.get(owner='frigg', name='frigg-hq', private=False)
        self.assertEqual(project.builds.all().count(), 1)
        self.assertEqual(project.builds.first().result.succeeded, False)

    def test_pull_request_handling(self, mock_start_build):
        response = self.post_webhook('pull_request', fixture='pull_request.json')
        self.assertStatusCode(response)
        self.assertEqual(
            Project.objects.filter(owner='tind', name='frigg', private=False).count(),
            1
        )
        mock_start_build.assert_called_once_with({
            'pull_request_id': 29,
            'author': 'relekang',
            'sha': 'fddd2887efd63196e48fd5d6bc0e62e1bafa0276',
            'branch': 'issue24-project-model',
            'message': 'Add model for projects\n### Todo:\r\n- [x] Fix templates\r\n- [x] '
                       'Add filtering of projects #30\r\n- [x] Add filtering of branches within '
                       'projects #30\r\n',
        })

    def test_pull_request_handling_open(self, mock_start_build):
        response = self.post_webhook('pull_request', fixture='pull_request_open.json')
        self.assertStatusCode(response)
        self.assertEqual(
            Project.objects.filter(owner='relekang', name='promised-ssh', private=False).count(),
            1
        )
        mock_start_build.assert_called_once_with({
            'pull_request_id': 3,
            'author': 'mcculloughsean',
            'sha': 'e3bb26f0fd87974f33e9809bd0eec51266b4fba1',
            'branch': 'master',
            'message': 'Add testing helpers\n',
        })

    def test_pull_request_handling_message(self, mock_start_build):
        response = self.post_webhook('pull_request', fixture='pull_request_no_message.json')
        self.assertStatusCode(response)
        self.assertEqual(
            Project.objects.filter(owner='tind', name='frigg', private=False).count(),
            1
        )
        mock_start_build.assert_called_once_with({
            'pull_request_id': 29,
            'author': 'relekang',
            'sha': 'fddd2887efd63196e48fd5d6bc0e62e1bafa0276',
            'branch': 'issue24-project-model',
            'message': 'Add model for projects\n',
        })

    def test_pull_request_handling_closed(self, mock_start_build):
        response = self.post_webhook('pull_request', fixture='pull_request_closed.json')
        self.assertStatusCode(response)
        self.assertFalse(mock_start_build.called)

    def test_pull_request_handling_labeled(self, mock_start_build):
        response = self.post_webhook('pull_request', fixture='pull_request_labeled.json')
        self.assertStatusCode(response)
        self.assertFalse(mock_start_build.called)

    def test_issue_comment_handling(self, mock_start_build):
        project = Project.objects.create(owner='tind', name='frigg', private=False)
        Build.objects.create(project=project, pull_request_id=29, author='relekang',
                             branch='issue24-project-model', message='Add model for projects\n',
                             sha='fddd2887efd63196e48fd5d6bc0e62e1bafa0276', build_number=1)
        response = self.post_webhook('issue_comment', fixture='issue_comment.json')
        self.assertStatusCode(response)
        mock_start_build.assert_called_once_with({
            'pull_request_id': 29,
            'author': 'relekang',
            'sha': 'fddd2887efd63196e48fd5d6bc0e62e1bafa0276',
            'branch': 'issue24-project-model',
            'message': 'Add model for projects\n',
        })

    def test_issue_comment_handling_regular_comment(self, mock_start_build):
        response = self.post_webhook('issue_comment', fixture='issue_comment_not_retest.json')
        self.assertStatusCode(response)
        self.assertFalse(mock_start_build.called)
