# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True,
                 primary_key=True)),
                ('git_repository', models.CharField(max_length=150,
                 verbose_name=b'git@github.com:owner/repo.git')),
                ('pull_request_id', models.IntegerField(default=0, max_length=150)),
                ('branch', models.CharField(default=b'master', max_length=100)),
                ('sha', models.CharField(max_length=150)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BuildResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True,
                 primary_key=True)),
                ('result_log', models.TextField()),
                ('succeeded', models.BooleanField(default=False)),
                ('return_code', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='build',
            name='result',
            field=models.OneToOneField(null=True, to='builds.BuildResult'),
            preserve_default=True,
        ),
    ]
