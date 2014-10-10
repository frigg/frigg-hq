# -*- coding: utf8 -*-
import os
import json
from unittest import skip

from django.conf import settings
from django.test import TestCase

from .github import parse_comment_payload, parse_push_payload, parse_pull_request_payload


class GithubHelpersTestCase(TestCase):
    def setUp(self):
        self.fixtures_path = os.path.join(settings.BASE_DIR, 'helpers/fixtures/github')

    def test_parse_issue_comment_payload(self):
        data = json.load(open(os.path.join(self.fixtures_path, 'issue_comment.json')))
        output = parse_comment_payload(data)

        self.assertEquals(output['repo_url'], 'git@github.com:tind/frigg.git')
        self.assertEquals(output['repo_owner'], 'tind')
        self.assertEquals(output['repo_name'], 'frigg')
        self.assertEquals(output['pull_request_id'], '29')

    def test_parse_pull_request_payload(self):
        data = json.load(open(os.path.join(self.fixtures_path, 'pull_request.json')))
        output = parse_pull_request_payload(data)

        self.assertEquals(output['repo_url'], 'git@github.com:tind/frigg.git')
        self.assertEquals(output['repo_owner'], 'tind')
        self.assertEquals(output['repo_name'], 'frigg')

    def test_parse_push_payload(self):
        data = json.load(open(os.path.join(self.fixtures_path, 'push.json')))
        output = parse_push_payload(data)

        self.assertEquals(output['repo_url'], 'git@github.com:tind/frigg.git')
        self.assertEquals(output['repo_owner'], 'tind')
        self.assertEquals(output['repo_name'], 'frigg')
        self.assertEquals(output['branch'], 'master')
        self.assertEquals(output['sha'], 'fddd2887efd63196e48fd5d6bc0e62e1bafa0276')
