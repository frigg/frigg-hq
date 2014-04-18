# coding=utf-8
import os
from fabric.decorators import task
from fabric.state import env
from django_fabric import App
import sys

sys.path.append(os.path.dirname(__file__))

env.user = 'ubuntu'
env.hosts = ['balder.tind.io']

site = App(
    project_paths={
        'prod': '/opt/frigg',
    },
    urls={
        'prod': 'https://frigg.tind.io/github-webhook/'
    },
    restart_command={
        'prod': 'sudo supervisorctl restart frigg'
    },
    project_package='frigg',
    test_settings='frigg.settings.test',
)

deploy = task(site.deploy)
test = task(site.test)

clone_prod_data = task(site.clone_data, "prod")