# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('owner', models.CharField(max_length=100, blank=True)),
                ('git_repository', models.CharField(help_text=b'git@github.com:owner/repo.git', max_length=150)),
                ('average_time', models.IntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='build',
            name='git_repository',
        ),
        migrations.AddField(
            model_name='build',
            name='build_number',
            field=models.IntegerField(default=0, db_index=True),
            preserve_default=False,
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
