# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0024_project_should_clone_with_ssh'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildresult',
            name='worker_host',
            field=models.CharField(null=True, blank=True, max_length=250),
        ),
    ]
