# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'project_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('git_repository', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('pull_request_id', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=150)),
            ('branch', self.gf('django.db.models.fields.CharField')(default='master', max_length=100)),
        ))
        db.send_create_signal(u'project', ['Project'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table(u'project_project')


    models = {
        u'project.project': {
            'Meta': {'object_name': 'Project'},
            'branch': ('django.db.models.fields.CharField', [], {'default': "'master'", 'max_length': '100'}),
            'git_repository': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pull_request_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '150'})
        }
    }

    complete_apps = ['project']