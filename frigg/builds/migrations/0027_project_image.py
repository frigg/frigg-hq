# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0026_buildresult_service_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.CharField(max_length=200, default=''),
        ),
    ]
