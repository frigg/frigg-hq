import pytest

from frigg.projects.models import EnvironmentVariable, Project


@pytest.fixture
def project():
    return Project(owner='frigg', name='frigg-hq')


def test_environment_variable__str__(project):
    variable = EnvironmentVariable(project=project, key='PYPI_PASSWORD')
    assert str(variable) == 'frigg / frigg-hq - PYPI_PASSWORD'
