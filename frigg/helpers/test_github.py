# -*- coding: utf8 -*-
from django.test import TransactionTestCase

from frigg.builds.models import Build, BuildResult, Project

from .github import _get_status_from_build, get_pull_request_url


class GithubHelpersTestCase(TransactionTestCase):

    def test__get_status_from_build(self):
        error = RuntimeError()
        build = Build.objects.create(build_number=1, branch='master', sha='sha')
        BuildResult.objects.create(build=build, result_log='result', succeeded=True)

        status = _get_status_from_build(build, True, None)[0]
        self.assertEqual(status, 'pending')
        status = _get_status_from_build(build, False, None)[0]
        self.assertEqual(status, 'success')
        status = _get_status_from_build(build, False, error)[0]
        self.assertEqual(status, 'error')
        build.result.succeeded = False
        build.result.save()
        status = _get_status_from_build(build, False, None)[0]
        self.assertEqual(status, 'failure')

    def test_get_pull_request_url(self):
        project = Project.objects.create(owner='frigg', name='frigg-worker')
        build = Build(project=project, branch='master')
        self.assertEqual(get_pull_request_url(build), 'https://github.com/frigg/frigg-worker')
        build = Build(project=project, branch='master', pull_request_id=1)
        self.assertEqual(get_pull_request_url(build),
                         'https://github.com/frigg/frigg-worker/pull/1')
