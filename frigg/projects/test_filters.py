from frigg.utils.tests import FiltersTestCase

from .filters import ProjectPermissionFilter
from .models import Project


class ProjectFilterTests(FiltersTestCase):
    fixtures = FiltersTestCase.fixtures + ['frigg/builds/fixtures/test_permitted_objects.yaml']

    def test_project_permitted_objects(self):
        self.filter_test_helper(ProjectPermissionFilter(), Project, 4, 3, 2)
