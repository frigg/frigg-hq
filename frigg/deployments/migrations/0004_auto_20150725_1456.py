# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deployments', '0003_prdeployment_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prdeployment',
            name='image',
            field=models.CharField(default='frigg/frigg-test-base', max_length=255),
        ),
    ]
