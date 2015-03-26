# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0012_remove_project_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='git_repository',
            field=models.CharField(unique=True, max_length=150, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=100, blank=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.CharField(max_length=100, blank=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together=set([('owner', 'name')]),
        ),
    ]
