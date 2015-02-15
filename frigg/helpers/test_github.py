# -*- coding: utf8 -*-
import json
import os

from django.conf import settings
from django.test import TestCase

from frigg.builds.models import Build, BuildResult, Project

from .github import (_get_status_from_build, get_pull_request_url, parse_comment_payload,
                     parse_member_payload, parse_ping_payload, parse_pull_request_payload,
                     parse_push_payload)


class GithubHelpersTestCase(TestCase):
    def setUp(self):
        self.fixtures_path = os.path.join(settings.BASE_DIR, 'helpers/fixtures/github')

    def test_parse_issue_comment_payload(self):
        data = json.load(open(os.path.join(self.fixtures_path, 'issue_comment.json'),
                              encoding='utf-8'))
        output = parse_comment_payload(data)

        self.assertEquals(output['repo_url'], 'git@github.com:tind/frigg.git')
        self.assertEquals(output['repo_owner'], 'tind')
        self.assertEquals(output['repo_name'], 'frigg')
        self.assertEquals(output['private'], False)
        self.assertEquals(output['pull_request_id'], 29)
        self.assertEquals(output['branch'], 'pr')
        self.assertEquals(output['sha'], '-')

        project = Project.objects.get_or_create_from_url('git@github.com:tind/frigg.git')
        Build.objects.create(project=project, pull_request_id=29, build_number=2, branch='issue28',
                             sha='h')
        output = parse_comment_payload(data)
        self.assertEquals(output['branch'], 'issue28')
        self.assertEquals(output['sha'], 'h')

    def test_parse_pull_request_payload(self):
        data = json.load(open(os.path.join(self.fixtures_path, 'pull_request.json'),
                              encoding='utf-8'))
        output = parse_pull_request_payload(data)

        self.assertEquals(output['repo_url'], 'git@github.com:tind/frigg.git')
        self.assertEquals(output['repo_owner'], 'tind')
        self.assertEquals(output['repo_name'], 'frigg')
        self.assertEquals(output['private'], False)
        self.assertEquals(
            output['message'],
            'Add model for projects\n'
            '### Todo:\r\n- [x] Fix templates\r\n- [x] Add filtering of projects #30\r\n'
            '- [x] Add filtering of branches within projects #30\r\n'
        )

    def test_parse_pull_request_payload_labeled(self):
        data = json.load(open(os.path.join(self.fixtures_path, 'pull_request_labeled.json'),
                              encoding='utf-8'))
        output = parse_pull_request_payload(data)

        self.assertEqual(output, None)

    def test_parse_pull_request_payload_closed(self):
        data = json.load(open(os.path.join(self.fixtures_path, 'pull_request_closed.json'),
                              encoding='utf-8'))
        output = parse_pull_request_payload(data)

        self.assertEqual(output, None)

    def test_parse_push_payload(self):
        data = json.load(open(os.path.join(self.fixtures_path, 'push_master.json'),
                              encoding='utf-8'))
        output = parse_push_payload(data)

        self.assertEquals(output['repo_url'], 'git@github.com:tind/frigg.git')
        self.assertEquals(output['repo_owner'], 'tind')
        self.assertEquals(output['repo_name'], 'frigg')
        self.assertEquals(output['branch'], 'master')
        self.assertEquals(output['private'], False)
        self.assertEquals(output['sha'], 'fddd2887efd63196e48fd5d6bc0e62e1bafa0276')
        self.assertEquals(
            output['message'],
            'Add Project model and automatically create projects\n\nrelated to #24'
        )

        data = json.load(open(os.path.join(self.fixtures_path, 'push_branch.json'),
                              encoding='utf-8'))
        self.assertIsNone(parse_push_payload(data))

    def test_parse_push_skip_payload(self):
        data = json.load(open(os.path.join(self.fixtures_path, 'push_master_skip.json'),
                              encoding='utf-8'))
        self.assertIsNone(parse_push_payload(data))

    def test_parse_ping_payload(self):
        data = json.load(open(os.path.join(self.fixtures_path, 'ping.json'),
                              encoding='utf-8'))
        output = parse_ping_payload(data)

        self.assertEquals(output['repo_url'], 'git@github.com:frigg/frigg.git')
        self.assertEquals(output['repo_owner'], 'frigg')
        self.assertEquals(output['repo_name'], 'frigg')
        self.assertEquals(output['private'], False)

    def test_parse_member_payload(self):
        data = json.load(open(os.path.join(self.fixtures_path, 'member.json'),
                              encoding='utf-8'))
        output = parse_member_payload(data)

        self.assertEquals(output['repo_url'], 'git@github.com:baxterthehacker/public-repo.git')
        self.assertEquals(output['repo_owner'], 'baxterthehacker')
        self.assertEquals(output['repo_name'], 'public-repo')
        self.assertEquals(output['username'], 'octocat')
        self.assertEquals(output['action'], 'added')

    def test__get_status_from_build(self):
        error = RuntimeError()
        build = Build.objects.create(build_number=1, branch='master', sha='sha')
        BuildResult.objects.create(build=build, result_log='result', succeeded=True, return_code=0)

        status = _get_status_from_build(build, True, None)[0]
        self.assertEqual(status, 'pending')
        status = _get_status_from_build(build, False, None)[0]
        self.assertEqual(status, 'success')
        status = _get_status_from_build(build, False, error)[0]
        self.assertEqual(status, 'error')
        build.result.succeeded = False
        build.result.return_code = 1
        build.result.save()
        status = _get_status_from_build(build, False, None)[0]
        self.assertEqual(status, 'failure')

    def test_get_pull_request_url(self):
        project = Project(owner='frigg', name='frigg-worker')
        build = Build(project=project, branch='master')
        self.assertEqual(get_pull_request_url(build), 'https://github.com/frigg/frigg-worker')
        build = Build(project=project, branch='master', pull_request_id=1)
        self.assertEqual(get_pull_request_url(build),
                         'https://github.com/frigg/frigg-worker/pull/1')
