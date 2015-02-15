from unittest.mock import Mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from .filters import BuildPermissionFilter, ProjectPermissionFilter
from .models import Build, Project


class FiltersTestCase(TestCase):
    fixtures = ['frigg/builds/fixtures/users.yaml',
                'frigg/builds/fixtures/test_permitted_objects.yaml']

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

    def test_project_permitted_objects(self):
        self.filter_test_helper(ProjectPermissionFilter(), Project, 4, 3, 2)

    def test_build_permitted_objects(self):
        self.filter_test_helper(BuildPermissionFilter(), Build, 5, 4, 2)
