# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prdeployment',
            name='docker_id',
            field=models.CharField(max_length=150, blank=True),
        ),
    ]
