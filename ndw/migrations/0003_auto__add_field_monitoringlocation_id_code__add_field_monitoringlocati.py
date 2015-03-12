# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MonitoringLocation.id_code'
        db.add_column(u'ndw_monitoringlocation', 'id_code',
                      self.gf('django.db.models.fields.CharField')(default=123, unique=True, max_length=100),
                      keep_default=False)

        # Adding field 'MonitoringLocation.latitude'
        db.add_column(u'ndw_monitoringlocation', 'latitude',
                      self.gf('django.db.models.fields.FloatField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MonitoringLocation.id_code'
        db.delete_column(u'ndw_monitoringlocation', 'id_code')

        # Deleting field 'MonitoringLocation.latitude'
        db.delete_column(u'ndw_monitoringlocation', 'latitude')


    models = {
        u'ndw.monitoringlocation': {
            'Meta': {'object_name': 'MonitoringLocation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['ndw']