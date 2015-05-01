# -*- coding: utf8 -*-
from django.db import models
from django.db.models import Q


class PermittedManager(models.Manager):

    def permitted_query(self, user):
        raise NotImplementedError

    def permitted(self, user):
        return self.filter(self.permitted_query(user)).distinct()


class ProjectManager(PermittedManager):

    def permitted_query(self, user):
        query = Q(private=False)
        if user.is_authenticated():
            query |= Q(members=user)
        return query
