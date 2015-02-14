# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0005_auto_20141120_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildresult',
            name='coverage',
            field=models.DecimalField(
                decimal_places=2,
                editable=False,
                blank=True,
                max_digits=5,
                null=True
            ),
            preserve_default=True,
        ),
    ]
