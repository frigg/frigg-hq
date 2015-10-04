# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import basis.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID',
                                        serialize=False)),
                ('created_at', models.DateTimeField(editable=False, default=basis.models._now)),
                ('updated_at', models.DateTimeField(editable=False, default=basis.models._now)),
                ('name', models.CharField(max_length=255)),
                ('version', models.CharField(max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
