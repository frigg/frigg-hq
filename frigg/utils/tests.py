# -*- coding: utf8 -*-
from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TransactionTestCase


class ViewTestCase(TransactionTestCase):
    fixtures = ['frigg/builds/fixtures/users.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)
        self.factory = RequestFactory()

    # def tearDown(self):
    #     get_user_model().objects.all().delete()

    def assertStatusCode(self, response, code=200):
        self.assertEqual(response.status_code, code)

    def add_request_fields(self, request, anonymous=False, superuser=False, staff=False):
        if anonymous:
            request.user = AnonymousUser()
        else:
            request.user = self.user
            request.user.is_superuser = superuser
            request.user.is_staff = staff

        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)


class FiltersTestCase(TransactionTestCase):
    fixtures = ['frigg/builds/fixtures/users.json']

    def setUp(self):
        self.user = get_user_model().objects.get(pk=1)

    def filter_test_helper(self, filter_instance, model, count_total, count_for_user,
                           count_for_anon):
        request = Mock()
        request.user = self.user
        self.assertEqual(model.objects.all().count(), count_total)
        self.assertEqual(
            filter_instance.filter_queryset(request, model.objects.all(), Mock()).count(),
            count_for_user
        )
        request.user = AnonymousUser()
        self.assertEqual(
            filter_instance.filter_queryset(request, model.objects.all(), Mock()).count(),
            count_for_anon
        )
