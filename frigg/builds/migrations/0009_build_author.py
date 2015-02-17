# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0008_auto_20150216_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='author',
            field=models.CharField(max_length=150, blank=True),
            preserve_default=True,
        ),
    ]
