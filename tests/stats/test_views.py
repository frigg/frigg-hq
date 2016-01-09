# -*- coding: utf8 -*-
from django.core.urlresolvers import reverse

from frigg.stats.views import overview
from frigg.utils.tests import ViewTestCase


class StatsSmokeViewTestCase(ViewTestCase):

    def test_overview_anonymous(self):
        request = self.factory.get(reverse('stats:overview'))
        self.add_request_fields(request, anonymous=True)
        response = overview(request)
        self.assertStatusCode(response, 302)

    def test_overview_regular_user(self):
        request = self.factory.get(reverse('stats:overview'))
        self.add_request_fields(request)
        response = overview(request)
        self.assertStatusCode(response, 302)

    def test_overview_staff_user(self):
        request = self.factory.get(reverse('stats:overview'))
        self.add_request_fields(request, staff=True)
        response = overview(request)
        self.assertStatusCode(response, 200)
