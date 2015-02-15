# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0006_buildresult_coverage'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='message',
            field=models.TextField(editable=False, blank=True, null=True),
            preserve_default=True,
        ),
    ]
