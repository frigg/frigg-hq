# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BuildResult'
        db.create_table(u'builds_buildresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('result_log', self.gf('django.db.models.fields.TextField')()),
            ('succeeded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('return_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'builds', ['BuildResult'])

        # Adding model 'Build'
        db.create_table(u'builds_build', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('git_repository', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('pull_request_id', self.gf('django.db.models.fields.IntegerField')(default=0,
                                                                                max_length=150)),
            ('branch', self.gf('django.db.models.fields.CharField')(default='master',
                                                                    max_length=100)),
            ('sha', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('result', self.gf('django.db.models.fields.related.OneToOneField')(
                to=orm['builds.BuildResult'],
                unique=True,
                null=True
            )),
        ))
        db.send_create_signal(u'builds', ['Build'])

    def backwards(self, orm):
        # Deleting model 'BuildResult'
        db.delete_table(u'builds_buildresult')

        # Deleting model 'Build'
        db.delete_table(u'builds_build')

    models = {
        u'builds.build': {
            'Meta': {'object_name': 'Build'},
            'branch': ('django.db.models.fields.CharField', [], {'default': "'master'",
                                                                 'max_length': '100'}),
            'git_repository': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pull_request_id': ('django.db.models.fields.IntegerField', [], {'default': '0',
                                                                             'max_length': '150'}),
            'result': ('django.db.models.fields.related.OneToOneField', [], {
                'to': u"orm['builds.BuildResult']",
                'unique': 'True',
                'null': 'True'
            }),
            'sha': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        u'builds.buildresult': {
            'Meta': {'object_name': 'BuildResult'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result_log': ('django.db.models.fields.TextField', [], {}),
            'return_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'succeeded': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['builds']
