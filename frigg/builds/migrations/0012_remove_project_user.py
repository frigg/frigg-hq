# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0011_auto_20150223_0442'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='user',
        ),
    ]
