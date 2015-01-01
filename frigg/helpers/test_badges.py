# -*- coding: utf-8 -*-
import unittest
from frigg.helpers.badges import _coverage_color


class BadgeHelperTestCase(unittest.TestCase):

    def test_coverage_color(self):
        self.assertEqual(_coverage_color(100), 'brightgreen')
        self.assertEqual(_coverage_color(92), 'green')
        self.assertEqual(_coverage_color(73), 'yellow')
        self.assertEqual(_coverage_color(55), 'orange')
        self.assertEqual(_coverage_color(42), 'red')
