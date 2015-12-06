# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('builds', '0030_auto_20151020_2008'),
    ]

    def convert_logs_to_json(apps, schema_editor):
        BuildResult = apps.get_model('builds', 'BuildResult')
        for result in BuildResult.objects.all():
            try:
                result.result_log = json.loads(result.result_log)
                result.setup_log = json.loads(result.setup_log)
                result.service_log = json.loads(result.service_log)
                result.save()
            except:
                print(result.pk)

    operations = [
        migrations.RunPython(convert_logs_to_json),
    ]
