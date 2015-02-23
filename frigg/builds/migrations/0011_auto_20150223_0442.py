# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0010_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='approved',
            field=models.BooleanField(default=False, db_index=True),
            preserve_default=True,
        ),
    ]
