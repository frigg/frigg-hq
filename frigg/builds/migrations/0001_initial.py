# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Build'
        db.create_table(u'builds_build', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('git_repository', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('pull_request_id', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=150)),
            ('branch', self.gf('django.db.models.fields.CharField')(default='master', max_length=100)),
            ('sha', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'builds', ['Build'])


    def backwards(self, orm):
        # Deleting model 'Build'
        db.delete_table(u'builds_build')


    models = {
        u'builds.build': {
            'Meta': {'object_name': 'Build'},
            'branch': ('django.db.models.fields.CharField', [], {'default': "'master'", 'max_length': '100'}),
            'git_repository': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pull_request_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '150'}),
            'sha': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['builds']