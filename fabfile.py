# coding=utf-8
from fabric.decorators import task
from fabric.state import env
from django_fabric import App

env.user = 'ubuntu'
env.hosts = ['balder.tind.io']

site = App(
    project_paths={
        'prod': '/opt/frigg',
        },
    urls={
        'prod': 'https://frigg.tind.io'
    },
    restart_command={
        'prod': 'supervisorctl restart frigg'
    },
    project_package='frigg',
    test_settings='settings',
)

deploy = task(site.deploy)
test = task(site.test)