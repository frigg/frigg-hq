# -*- coding: utf8 -*-
from django.contrib.staticfiles import finders
from django.core.cache import cache


def get_badge(succeeded):
    badge = cache.get('badge%s' % succeeded)
    if badge is None:
        if succeeded:
            path = finders.find('badges/build-success.svg')
        else:
            path = finders.find('badges/build-failure.svg')

        with open(path) as f:
            badge = f.read()
            cache.set('badge%s' % succeeded, badge, timeout=60 * 60 * 24 * 7)
    return badge
