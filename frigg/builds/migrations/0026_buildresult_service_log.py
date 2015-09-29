# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0025_buildresult_worker_host'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildresult',
            name='service_log',
            field=models.TextField(blank=True),
        ),
    ]
