from frigg.builds.filters import BuildPermissionFilter
from frigg.builds.models import Build
from frigg.utils.tests import FiltersTestCase


class BuildsFilterTests(FiltersTestCase):
    fixtures = FiltersTestCase.fixtures + ['frigg/builds/fixtures/test_permitted_objects.yaml']

    def test_build_permitted_objects(self):
        self.filter_test_helper(BuildPermissionFilter(), Build, 5, 4, 2)
