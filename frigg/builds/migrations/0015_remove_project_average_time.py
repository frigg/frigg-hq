# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0014_project_queue_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='average_time',
        ),
    ]
