# -*- coding: utf-8 -*-


from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0002_auto_20141028_0710'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='build',
            options={'ordering': ['-id']},
        ),
    ]
