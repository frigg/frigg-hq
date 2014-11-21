# -*- coding: utf8 -*-
from django.core.urlresolvers import reverse

from frigg.utils.tests import ViewTestCase
from .views import overview


class StatsSmokeViewTestCase(ViewTestCase):

    def test_overview_anonymous(self):
        request = self.factory.get(reverse('overview'))
        self.add_request_fields(request, anonymous=True)
        response = overview(request)
        self.assertStatusCode(response, 302)

    def test_overview_regular_user(self):
        request = self.factory.get(reverse('overview'))
        self.add_request_fields(request)
        response = overview(request)
        self.assertStatusCode(response, 302)

    def test_overview_staff_user(self):
        request = self.factory.get(reverse('overview'))
        self.add_request_fields(request, staff=True)
        response = overview(request)
        self.assertStatusCode(response, 200)
