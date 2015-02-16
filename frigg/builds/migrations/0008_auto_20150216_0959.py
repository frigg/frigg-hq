# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0007_build_message'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['owner', 'name']},
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='projects', null=True, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
