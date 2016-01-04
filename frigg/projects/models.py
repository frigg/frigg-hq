from django.db import models

from frigg.builds.models import Project  # noqa


class EnvironmentVariable(models.Model):
    project = models.ForeignKey(Project, related_name='environment_variables')
    key = models.CharField(max_length=200)
    value = models.TextField()
    is_secret = models.BooleanField(default=True)

    def __str__(self):
        return '{project} - {key}'.format(project=self.project, key=self.key)
