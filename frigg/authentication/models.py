# -*- coding: utf8 -*-
from django.contrib.auth.models import AbstractUser
from django.utils.functional import cached_property
from social.apps.django_app.default.models import UserSocialAuth

from frigg.helpers import github


class User(AbstractUser):

    @cached_property
    def github_token(self):
        try:
            return self.social_auth.get(provider='github').extra_data['access_token']
        except UserSocialAuth.DoesNotExist:
            return

    def save(self, *args, **kwargs):
        create = self.pk is None
        super(User, self).save(*args, **kwargs)
        if create:
            self.update_repo_permissions()

    def update_repo_permissions(self):
        if self.github_token:
            github.update_repo_permissions(self)
