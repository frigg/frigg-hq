# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0019_auto_20150408_0658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='build',
            name='build_number',
            field=models.IntegerField(db_index=True, default=0, null=True),
        ),
    ]
