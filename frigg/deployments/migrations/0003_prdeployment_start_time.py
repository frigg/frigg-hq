# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0002_prdeployment_docker_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='prdeployment',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
