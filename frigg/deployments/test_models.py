import json
from unittest import mock

from django.test import TestCase

from frigg.builds.models import Build, Project
from frigg.deployments.models import PRDeployment


class PRDeploymentTestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/users.json']

    def setUp(self):
        project = Project.objects.create(owner='frigg', name='frigg-hq')
        build = Build.objects.create(project=project, build_number=1)
        self.deployment = PRDeployment.objects.create(build=build, port=50000, image='ubuntu')

    def test___str__(self):
        self.assertEqual(str(self.deployment), 'Deployment: frigg / frigg-hq / master #1')

    def test_get_deployment_url(self):
        self.assertEqual(self.deployment.get_deployment_url(), 'http://50000.pr.frigg.io')

    def test_ttl(self):
        self.assertEqual(self.deployment.ttl, 1800)

    def test_is_pending_should_be_true(self):
        self.assertTrue(self.deployment.is_pending)

    def test_is_pending_should_be_false_if_deploy_failed(self):
        self.deployment.succeeded = False
        self.assertFalse(self.deployment.is_pending)

    def test_is_pending_should_be_false_if_deploy_succeeded(self):
        self.deployment.succeeded = True
        self.assertFalse(self.deployment.is_pending)

    def test_queue_object_should_contain_correct_information(self):
        self.assertEqual(self.deployment.queue_object['port'], 50000)
        self.assertEqual(self.deployment.queue_object['image'], 'ubuntu')
        self.assertEqual(self.deployment.queue_object['ttl'], 1800)

    def test_tasks_with_empty_log(self):
        self.assertEqual(self.deployment.tasks, [])

    def test_tasks_with_json_log(self):
        self.deployment.log = '[{"task":"apt-get install nginx","output":"Installed",' \
                              '"succeeded":true}]'
        self.assertEqual(len(self.deployment.tasks), 1)
        self.assertEqual(self.deployment.tasks[0]['task'], 'apt-get install nginx')

    @mock.patch('frigg.helpers.github.set_commit_status')
    def test_handle_report_should_save_log(self, mock_set_commit_status):
        report = [
            {'task': 'apt-get install nginx', 'output': 'Installed', 'succeeded': True},
            {'task': 'pip install gunicorn', 'output': 'Installed', 'succeeded': True}
        ]
        self.deployment.handle_report({'results': report})
        deployment = PRDeployment.objects.get(pk=self.deployment.pk)
        self.assertEqual(deployment.log, json.dumps(report))

    @mock.patch('frigg.helpers.github.set_commit_status')
    def test_handle_report_which_succeeded(self, mock_set_commit_status):
        report = [
            {'task': 'apt-get install nginx', 'output': 'Installed', 'succeeded': True},
            {'task': 'pip install gunicorn', 'output': 'Installed', 'succeeded': True}
        ]
        self.deployment.handle_report({'results': report})
        deployment = PRDeployment.objects.get(pk=self.deployment.pk)
        self.assertTrue(deployment.succeeded)
        mock_set_commit_status.assert_called_once_with(deployment.build, context='frigg-preview')

    @mock.patch('frigg.helpers.github.set_commit_status')
    def test_handle_report_which_fails(self, mock_set_commit_status):
        report = [
            {'task': 'apt-get install nginx', 'output': 'Installed', 'succeeded': True},
            {'task': 'pip install gunicorn', 'output': 'Unknown package', 'succeeded': False}
        ]
        self.deployment.handle_report({'results': report})
        deployment = PRDeployment.objects.get(pk=self.deployment.pk)
        self.assertFalse(deployment.succeeded)
        mock_set_commit_status.assert_called_once_with(deployment.build, context='frigg-preview')

    @mock.patch('frigg.helpers.github.set_commit_status')
    def test_handle_report_with_pending_result(self, mock_set_commit_status):
        report = [
            {'task': 'apt-get install nginx', 'output': 'Installed', 'succeeded': True},
            {'task': 'pip install gunicorn', 'pending': True}
        ]
        self.deployment.handle_report({'results': report})
        deployment = PRDeployment.objects.get(pk=self.deployment.pk)
        self.assertIsNone(deployment.succeeded)
        self.assertFalse(mock_set_commit_status.called)
