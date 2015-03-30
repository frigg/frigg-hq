# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0016_remove_buildresult_return_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildresult',
            name='still_running',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
