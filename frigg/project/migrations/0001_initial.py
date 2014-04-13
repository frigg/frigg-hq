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
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('repo_git', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal(u'project', ['Project'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table(u'project_project')


    models = {
        u'project.project': {
            'Meta': {'object_name': 'Project'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'repo_git': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['project']