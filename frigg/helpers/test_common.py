# -*- coding: utf8 -*-
from django.test import TestCase
from frigg.helpers.common import is_retest_comment


class HelperTestCase(TestCase):

    def test_is_retest_comment(self):
        self.assertFalse(is_retest_comment(''))
        self.assertTrue(is_retest_comment('retest now please'))
        self.assertTrue(is_retest_comment('Retest now please'))
        self.assertTrue(is_retest_comment('retest this please'))
        self.assertTrue(is_retest_comment('Retest this please'))
        self.assertTrue(is_retest_comment('retest now'))
        self.assertTrue(is_retest_comment('Retest now'))
        self.assertTrue(is_retest_comment('retest this'))
        self.assertTrue(is_retest_comment('Retest this'))
        self.assertTrue(is_retest_comment('retest please'))
        self.assertTrue(is_retest_comment('Retest please'))
