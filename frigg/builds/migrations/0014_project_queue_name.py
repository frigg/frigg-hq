# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0013_auto_20150325_2210'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='queue_name',
            field=models.CharField(default='frigg:queue', max_length=200),
            preserve_default=True,
        ),
    ]
