# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0021_remove_project_git_repository'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildresult',
            name='setup_log',
            field=models.TextField(blank=True),
        ),
    ]
