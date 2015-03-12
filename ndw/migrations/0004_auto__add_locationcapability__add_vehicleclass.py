# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LocationCapability'
        db.create_table(u'ndw_locationcapability', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ndw.MonitoringLocation'])),
            ('lane_type', self.gf('django.db.models.fields.IntegerField')()),
            ('capability_index', self.gf('django.db.models.fields.IntegerField')()),
            ('measurement_type', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('vehicle_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ndw.VehicleClass'])),
        ))
        db.send_create_signal(u'ndw', ['LocationCapability'])

        # Adding model 'VehicleClass'
        db.create_table(u'ndw_vehicleclass', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('length_from', self.gf('django.db.models.fields.FloatField')()),
            ('length_to', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'ndw', ['VehicleClass'])


    def backwards(self, orm):
        # Deleting model 'LocationCapability'
        db.delete_table(u'ndw_locationcapability')

        # Deleting model 'VehicleClass'
        db.delete_table(u'ndw_vehicleclass')


    models = {
        u'ndw.locationcapability': {
            'Meta': {'object_name': 'LocationCapability'},
            'capability_index': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lane_type': ('django.db.models.fields.IntegerField', [], {}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ndw.MonitoringLocation']"}),
            'measurement_type': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'vehicle_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['ndw.VehicleClass']"})
        },
        u'ndw.monitoringlocation': {
            'Meta': {'object_name': 'MonitoringLocation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
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