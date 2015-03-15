# -*- coding: utf8 -*-
import requests
from django.contrib.staticfiles import finders
from django.core.cache import cache


def get_badge(succeeded):
    key = 'badge{}'.format(succeeded)
    badge = cache.get(key)
    if badge is None:
        if succeeded:
            path = finders.find('badges/build-success.svg')
        else:
            path = finders.find('badges/build-failure.svg')

        with open(path) as f:
            badge = f.read()
            cache.set(key, badge, timeout=60 * 60 * 24 * 7)
    return badge


def get_coverage_badge(coverage):
    key = 'badgecoverage{}'.format(coverage)
    badge = cache.get(key)
    if badge is None:
        if coverage is None:
            url = 'https://img.shields.io/badge/coverage-unknown-lightgrey.svg'
        else:
            url = 'https://img.shields.io/badge/coverage-{}%-{}.svg?style=flat'.format(
                coverage,
                _coverage_color(coverage)
            )
        badge = requests.get(url).text
        cache.set(key, badge)
    return badge


def _coverage_color(coverage):
    if coverage == 100:
        return 'brightgreen'
    if coverage >= 90:
        return 'green'
    if coverage >= 70:
        return 'yellow'
    if coverage >= 50:
        return 'orange'
    return 'red'
