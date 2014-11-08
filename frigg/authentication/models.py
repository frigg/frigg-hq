# -*- coding: utf8 -*-
from django.contrib.auth.models import AbstractUser
from django.db import models

from frigg.helpers import github


class User(AbstractUser):
    github_token = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        create = hasattr(self, 'id')
        super(User, self).save(*args, **kwargs)
        if create:
            self.update_repo_permissions()

    def update_repo_permissions(self):
        if self.github_token:
            github.update_repo_permissions(self)