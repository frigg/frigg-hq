import pytest
from django.core.management import call_command

from frigg.builds.models import Project, Build


@pytest.fixture
def build():
    project = Project.objects.create(owner='tind', name='frigg', approved=False)
    return Build.objects.create(project=project, branch='master', build_number=1)


@pytest.mark.django_db
def test_restart_should_call_restart_when_force_is_false(mocker, build):
    mock_start = mocker.patch('frigg.builds.models.Build.start')
    mock_restart = mocker.patch('frigg.builds.models.Build.restart')
    call_command('restart_builds')
    assert mock_restart.called
    assert not mock_start.called


@pytest.mark.django_db
def test_restart_should_call_start_when_force_is_true(mocker, build):
    mock_start = mocker.patch('frigg.builds.models.Build.start')
    mock_restart = mocker.patch('frigg.builds.models.Build.restart')
    call_command('restart_builds', force=True)
    assert mock_start.called
    assert not mock_restart.called
