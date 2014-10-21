# -*- coding: utf8 -*-
from unittest import TestCase
from frigg.builds.helpers import _detect_test_runners


class HelpersTestCase(TestCase):
    def test__detect_test_runners(self):
        self.assertEqual(_detect_test_runners([]), [])
        files = ['_config.yml', 'Cargo.toml', 'build.sbt', 'package.json', 'manage.py', 'setup.py',
                 'tox.ini', 'Makefile']
        self.assertEqual(_detect_test_runners(files), ['make test'])
        del files[len(files) - 1]
        self.assertEqual(_detect_test_runners(files), ['tox', 'flake8'])
        del files[len(files) - 1]
        self.assertEqual(_detect_test_runners(files), ['python setup.py test', 'flake8'])
        del files[len(files) - 1]
        self.assertEqual(_detect_test_runners(files), ['python manage.py test', 'flake8'])
        del files[len(files) - 1]
        self.assertEqual(_detect_test_runners(files), ['npm test'])
        del files[len(files) - 1]
        self.assertEqual(_detect_test_runners(files), ['sbt test'])
        del files[len(files) - 1]
        self.assertEqual(_detect_test_runners(files), ['cargo test'])
        del files[len(files) - 1]
        self.assertEqual(_detect_test_runners(files), ['jekyll build'])
        del files[len(files) - 1]
        self.assertEqual(_detect_test_runners(files), [])
