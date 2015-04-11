# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0019_auto_20150408_0658'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='can_deploy',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
