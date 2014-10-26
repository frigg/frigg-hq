# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0003_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='build',
            name='is_pending',
        ),
    ]
