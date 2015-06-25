# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0023_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='should_clone_with_ssh',
            field=models.BooleanField(default=False),
        ),
    ]
