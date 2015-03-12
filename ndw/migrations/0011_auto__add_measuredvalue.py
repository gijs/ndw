# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MeasuredValue'
        db.create_table(u'ndw_measuredvalue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location_capability', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ndw.LocationCapability'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('input_values_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('standard_deviation', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal(u'ndw', ['MeasuredValue'])


    def backwards(self, orm):
        # Deleting model 'MeasuredValue'
        db.delete_table(u'ndw_measuredvalue')


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
            'vehicle_length_from': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'vehicle_length_to': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        },
        u'ndw.measuredvalue': {
            'Meta': {'object_name': 'MeasuredValue'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_values_number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'location_capability': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ndw.LocationCapability']"}),
            'standard_deviation': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
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