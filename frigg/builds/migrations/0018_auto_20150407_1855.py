# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0017_buildresult_still_running'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='pull_request_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='project',
            name='members',
            field=models.ManyToManyField(related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
    ]
