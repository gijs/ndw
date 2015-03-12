# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'LocationCapability.measurement_type'
        db.alter_column(u'ndw_locationcapability', 'measurement_type', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'LocationCapability.lane_type'
        db.alter_column(u'ndw_locationcapability', 'lane_type', self.gf('django.db.models.fields.CharField')(max_length=2))

    def backwards(self, orm):

        # Changing field 'LocationCapability.measurement_type'
        db.alter_column(u'ndw_locationcapability', 'measurement_type', self.gf('django.db.models.fields.CharField')(max_length=2))

        # Changing field 'LocationCapability.lane_type'
        db.alter_column(u'ndw_locationcapability', 'lane_type', self.gf('django.db.models.fields.IntegerField')())

    models = {
        u'ndw.locationcapability': {
            'Meta': {'object_name': 'LocationCapability'},
            'accuracy': ('django.db.models.fields.FloatField', [], {'default': '100'}),
            'capability_index': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lane_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ndw.MonitoringLocation']"}),
            'measurement_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'period': ('django.db.models.fields.IntegerField', [], {'default': '60'}),
            'vehicle_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ndw.VehicleClass']"})
        },
        u'ndw.monitoringlocation': {
            'Meta': {'object_name': 'MonitoringLocation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'lanes_number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
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