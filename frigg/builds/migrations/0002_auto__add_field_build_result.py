# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Build.result'
        db.add_column(u'builds_build', 'result',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Build.result'
        db.delete_column(u'builds_build', 'result')


    models = {
        u'builds.build': {
            'Meta': {'object_name': 'Build'},
            'branch': ('django.db.models.fields.CharField', [], {'default': "'master'", 'max_length': '100'}),
            'git_repository': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pull_request_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '150'}),
            'result': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'sha': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['builds']