# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0018_auto_20150407_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, related_name='projects'),
        ),
    ]
