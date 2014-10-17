# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('builds', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(
                related_name=b'auth_projects',
                blank=True,
                null=True,
                to=settings.AUTH_USER_MODEL,
                help_text=b'A user with access to the repository.'
            )
        ),
    ]
