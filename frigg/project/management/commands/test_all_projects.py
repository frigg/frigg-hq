# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand
from frigg.project.models import Project


class Command(BaseCommand):

    def handle(self, *args, **options):
        for project in Project.objects.all():
            project.run_tests()