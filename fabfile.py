# -*- coding: utf8 -*-
import os
import sys

from fabric.decorators import task
from fabric.state import env
from django_fabric import App

from fab_local import settings

sys.path.append(os.path.dirname(__file__))

env.user = settings['USER']
env.hosts = [settings['HOST']]


class FriggApp(App):
    project_package = 'frigg'
    test_settings = 'frigg.settings.test'


site = FriggApp(
    project_paths=settings['PROJECT_PATHS'],
    urls=settings['URL'],
    restart_command=settings['RESTART_COMMAND'],
)


deploy = task(site.deploy)
test = task(site.test)
clone_data = task(site.clone_data, "prod")
