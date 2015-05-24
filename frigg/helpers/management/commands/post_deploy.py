import subprocess

from django.core.cache import cache
from django.core.management import BaseCommand


def set_git_short_ref():
    cache.set(
        'gitref',
        subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']),
        60 * 60 * 365
    )


class Command(BaseCommand):

    help = 'Reset cache etc.'

    def handle(self, *args, **options):
        set_git_short_ref()
