# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BuildResult'
        db.create_table(u'builds_buildresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stdout', self.gf('django.db.models.fields.TextField')()),
            ('stderr', self.gf('django.db.models.fields.TextField')()),
            ('succeeded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('return_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'builds', ['BuildResult'])


        # Renaming column for 'Build.result' to match new field type.
        db.rename_column(u'builds_build', 'result', 'result_id')
        # Changing field 'Build.result'
        db.alter_column(u'builds_build', 'result_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['builds.BuildResult'], unique=True, null=True))
        # Adding index on 'Build', fields ['result']
        db.create_index(u'builds_build', ['result_id'])

        # Adding unique constraint on 'Build', fields ['result']
        db.create_unique(u'builds_build', ['result_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Build', fields ['result']
        db.delete_unique(u'builds_build', ['result_id'])

        # Removing index on 'Build', fields ['result']
        db.delete_index(u'builds_build', ['result_id'])

        # Deleting model 'BuildResult'
        db.delete_table(u'builds_buildresult')


        # Renaming column for 'Build.result' to match new field type.
        db.rename_column(u'builds_build', 'result_id', 'result')
        # Changing field 'Build.result'
        db.alter_column(u'builds_build', 'result', self.gf('django.db.models.fields.TextField')())

    models = {
        u'builds.build': {
            'Meta': {'object_name': 'Build'},
            'branch': ('django.db.models.fields.CharField', [], {'default': "'master'", 'max_length': '100'}),
            'git_repository': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pull_request_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '150'}),
            'result': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['builds.BuildResult']", 'unique': 'True', 'null': 'True'}),
            'sha': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'builds.buildresult': {
            'Meta': {'object_name': 'BuildResult'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'return_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'stderr': ('django.db.models.fields.TextField', [], {}),
            'stdout': ('django.db.models.fields.TextField', [], {}),
            'succeeded': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['builds']