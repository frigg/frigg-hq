# coding=utf-8
from fabric.decorators import task
from fabric.state import env
from django_fabric import App

env.user = 'ubuntu'
env.hosts = ['frigg.tind.io']

site = App(
    project_paths={
        'prod': '/opt/frigg',
        },
    urls={
        'prod': 'https://frigg.tind.io'
    },
    restart_command={
        'prod': 'restart prod'
    },
    project_package='frigg',
    test_settings='frigg.settings.test',
)

deploy = task(site.deploy)
test = task(site.test)