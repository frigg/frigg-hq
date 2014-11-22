# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0004_auto_20141114_1336'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='build',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
