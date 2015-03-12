# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MonitoringLocation'
        db.create_table(u'ndw_monitoringlocation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'ndw', ['MonitoringLocation'])


    def backwards(self, orm):
        # Deleting model 'MonitoringLocation'
        db.delete_table(u'ndw_monitoringlocation')


    models = {
        u'ndw.monitoringlocation': {
            'Meta': {'object_name': 'MonitoringLocation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['ndw']