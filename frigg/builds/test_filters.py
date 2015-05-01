from frigg.utils.tests import FiltersTestCase

from .filters import BuildPermissionFilter
from .models import Build


class BuildsFilterTests(FiltersTestCase):
    fixtures = FiltersTestCase.fixtures + ['frigg/builds/fixtures/test_permitted_objects.yaml']

    def test_build_permitted_objects(self):
        self.filter_test_helper(BuildPermissionFilter(), Build, 5, 4, 2)
