from basis.models import TimeStampModel
from django.db import models


class Worker (TimeStampModel):
    name = models.CharField(max_length=255)
    version = models.CharField(max_length=10)

    def __str__(self):
        return self.name
