# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'LocationCapability.vehicle_class'
        db.delete_column(u'ndw_locationcapability', 'vehicle_class_id')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'LocationCapability.vehicle_class'
        raise RuntimeError("Cannot reverse this migration. 'LocationCapability.vehicle_class' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'LocationCapability.vehicle_class'
        db.add_column(u'ndw_locationcapability', 'vehicle_class',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ndw.VehicleClass']),
                      keep_default=False)


    models = {
        u'ndw.locationcapability': {
            'Meta': {'object_name': 'LocationCapability'},
            'accuracy': ('django.db.models.fields.FloatField', [], {'default': '100'}),
            'capability_index': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lane_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ndw.MonitoringLocation']"}),
            'measurement_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'period': ('django.db.models.fields.IntegerField', [], {'default': '60'})
        },
        u'ndw.monitoringlocation': {
            'Meta': {'object_name': 'MonitoringLocation'},
            'end_latitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'end_longitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'lanes_number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'length_affected': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {})
        },
        u'ndw.vehicleclass': {
            'Meta': {'object_name': 'VehicleClass'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length_from': ('django.db.models.fields.FloatField', [], {}),
            'length_to': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['ndw']