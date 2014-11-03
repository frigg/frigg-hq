# -*- coding: utf8 -*-
import re

from django.db import models
from django.db.models import Q


class ProjectManager(models.Manager):
    def get_or_create_from_url(self, url):
        item, created = self.get_or_create(git_repository=url)
        if created:
            rex = "git@github.com:([\w\.-]*)/([\w\.-]*).git"
            match = re.match(rex, item.git_repository)
            item.owner = match.group(1)
            item.name = match.group(2)
            item.save()
        return item

    def permitted(self, user):
        return self.filter(Q(private=False) | Q(members=user))


class BuildManager(models.Manager):
    def permitted(self, user):
        return self.filter(Q(project__private=False) | Q(project__members=user))


class BuildResultManager(models.Manager):
    def permitted(self, user):
        return self.filter(Q(build__project__private=False) | Q(build__project__members=user))
