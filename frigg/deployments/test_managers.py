from django.test import TestCase

from frigg.builds.models import Build, Project

from .models import PRDeployment


class PRDeploymentManagerTests(TestCase):

    def setUp(self):
        project = Project.objects.create(owner='frigg', name='frigg-hq')
        build = Build.objects.create(project=project, build_number=1)
        PRDeployment.objects.create(build=build, image='ubuntu')
        self.build = Build.objects.create(project=project, build_number=2)

    def test_create_should_not_override_port_in_kwargs(self):
        deployment = PRDeployment.objects.create(build=self.build, image='ubuntu', port=50000)
        self.assertEqual(deployment.port, 50000)

    def test_create_should_set_port_if_not_in_kwargs(self):
        deployment = PRDeployment.objects.create(build=self.build, image='ubuntu')
        self.assertEqual(deployment.port, 49153)

    def test_create_should_set_port_to_49152_if_it_is_to_high(self):
        deployment = PRDeployment.objects.create(build=self.build, image='ubuntu', port=65536)
        self.assertEqual(deployment.port, 49152)

    def test_create_should_set_port_to_49152_if_it_is_to_low(self):
        deployment = PRDeployment.objects.create(build=self.build, image='ubuntu', port=49151)
        self.assertEqual(deployment.port, 49152)
