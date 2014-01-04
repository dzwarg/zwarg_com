# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Path'
        db.create_table(u'geo_path', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')()),
        ))
        db.send_create_signal(u'geo', ['Path'])


    def backwards(self, orm):
        # Deleting model 'Path'
        db.delete_table(u'geo_path')


    models = {
        u'geo.path': {
            'Meta': {'object_name': 'Path'},
            'geom': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['geo']