# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Build',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True,
                 primary_key=True)),
                ('build_number', models.IntegerField(db_index=True)),
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
                ('build', models.OneToOneField(related_name=b'result', to='builds.Build')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True,
                 primary_key=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('owner', models.CharField(max_length=100, blank=True)),
                ('git_repository', models.CharField(max_length=150)),
                ('average_time', models.IntegerField(null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL,
                 help_text=b'A user with access to the repository.', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='build',
            name='project',
            field=models.ForeignKey(related_name=b'builds', to='builds.Project', null=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='build',
            unique_together=set([('project', 'build_number')]),
        ),
    ]
