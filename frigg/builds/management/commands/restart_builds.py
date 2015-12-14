# -*- coding: utf8 -*-
from django.core.management.base import BaseCommand

from frigg.builds.models import Build


class Command(BaseCommand):

    help = 'Restarts all builds that seems to have timed out.'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', dest='force', default=False)

    def handle(self, *args, **options):
        for build in Build.objects.filter(result=None):
            if build.has_timed_out():
                if options['force']:
                    build.start()
                else:
                    build.restart()
