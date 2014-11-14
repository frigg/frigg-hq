# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import basis.models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0003_auto_20141029_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='build',
            name='created_at',
            field=models.DateTimeField(editable=False, default=basis.models._now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='build',
            name='updated_at',
            field=models.DateTimeField(editable=False, default=basis.models._now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buildresult',
            name='created_at',
            field=models.DateTimeField(editable=False, default=basis.models._now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buildresult',
            name='updated_at',
            field=models.DateTimeField(editable=False, default=basis.models._now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='created_at',
            field=models.DateTimeField(editable=False, default=basis.models._now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(editable=False, default=basis.models._now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='build',
            name='branch',
            field=models.CharField(max_length=100, default='master'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='project',
            name='user',
            field=models.ForeignKey(
                related_name='authx1_projects',
                help_text='A user with access to the repository.',
                null=True,
                to=settings.AUTH_USER_MODEL,
                blank=True
            ),
            preserve_default=True,
        ),
    ]
