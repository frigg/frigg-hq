# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0020_auto_20150412_1200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='git_repository',
        ),
    ]
