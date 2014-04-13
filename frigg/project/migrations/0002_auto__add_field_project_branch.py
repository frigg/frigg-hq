# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.branch'
        db.add_column(u'project_project', 'branch',
                      self.gf('django.db.models.fields.CharField')(default='master', max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.branch'
        db.delete_column(u'project_project', 'branch')


    models = {
        u'project.project': {
            'Meta': {'object_name': 'Project'},
            'branch': ('django.db.models.fields.CharField', [], {'default': "'master'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'repo_git': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        }
    }

    complete_apps = ['project']