# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(verbose_name='email address', max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(
                help_text='The groups this user belongs to. A user will get all permissions'
                          ' granted to each of their groups.',
                verbose_name='groups',
                related_query_name='user',
                to='auth.Group',
                related_name='user_set',
                blank=True
            ),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(verbose_name='last login', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.',
                unique=True,
                max_length=30,
                verbose_name='username',
                validators=[django.core.validators.RegexValidator(
                    '^[\\w.@+-]+$',
                    'Enter a valid username. This value may contain only letters, '
                    'numbers and @/./+/-/_ characters.', 'invalid'
                )],
                error_messages={'unique': 'A user with that username already exists.'}
            ),
        ),
    ]
