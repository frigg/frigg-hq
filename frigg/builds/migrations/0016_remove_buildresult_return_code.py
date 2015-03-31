# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0015_remove_project_average_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='buildresult',
            name='return_code',
        ),
    ]
