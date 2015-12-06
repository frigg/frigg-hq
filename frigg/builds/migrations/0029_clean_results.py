# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('builds', '0028_auto_20151016_1928'),
    ]

    def clean(apps, schema_editor):
        BuildResult = apps.get_model('builds', 'BuildResult')
        for result in BuildResult.objects.filter(result_log='Branch deleted before built'):
            result.result_log = '[{"task": "", "error": "Branch deleted before built"}]'
            result.save()

        for result in BuildResult.objects.all():
            try:
                a = json.loads(result.result_log)  # noqa
                b = json.loads(result.setup_log)  # noqa
                c = json.loads(result.service_log)  # noqa
            except Exception:
                print(result.pk)
                if len(result.result_log) == 0:
                    result.result_log = '[]'
                if len(result.service_log) == 0:
                    result.service_log = '[]'
                if len(result.setup_log) == 0:
                    result.setup_log = '[]'

                result.save()

    operations = [
        migrations.RunPython(clean),
    ]
