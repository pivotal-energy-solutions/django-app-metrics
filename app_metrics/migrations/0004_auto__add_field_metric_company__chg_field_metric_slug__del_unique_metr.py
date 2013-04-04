# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Gauge', fields ['slug']
        db.delete_unique('app_metrics_gauge', ['slug'])

        # Removing unique constraint on 'Metric', fields ['slug']
        db.delete_unique('app_metrics_metric', ['slug'])

        # Adding field 'Metric.company'
        db.add_column('app_metrics_metric', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['company.Company'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Metric.slug'
        db.alter_column('app_metrics_metric', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=128))

        # Changing field 'Metric.name'
        db.alter_column('app_metrics_metric', 'name', self.gf('django.db.models.fields.CharField')(max_length=128))
        # Adding unique constraint on 'Metric', fields ['company', 'slug']
        db.create_unique('app_metrics_metric', ['company_id', 'slug'])


        # Changing field 'MetricSet.name'
        db.alter_column('app_metrics_metricset', 'name', self.gf('django.db.models.fields.CharField')(max_length=128))
        # Adding field 'Gauge.company'
        db.add_column('app_metrics_gauge', 'company',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['company.Company'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Gauge.name'
        db.alter_column('app_metrics_gauge', 'name', self.gf('django.db.models.fields.CharField')(max_length=128))

        # Changing field 'Gauge.slug'
        db.alter_column('app_metrics_gauge', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=128))

    def backwards(self, orm):
        # Removing unique constraint on 'Metric', fields ['company', 'slug']
        db.delete_unique('app_metrics_metric', ['company_id', 'slug'])

        # Deleting field 'Metric.company'
        db.delete_column('app_metrics_metric', 'company_id')


        # Changing field 'Metric.slug'
        db.alter_column('app_metrics_metric', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=60, unique=True))
        # Adding unique constraint on 'Metric', fields ['slug']
        db.create_unique('app_metrics_metric', ['slug'])


        # Changing field 'Metric.name'
        db.alter_column('app_metrics_metric', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'MetricSet.name'
        db.alter_column('app_metrics_metricset', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Deleting field 'Gauge.company'
        db.delete_column('app_metrics_gauge', 'company_id')


        # Changing field 'Gauge.name'
        db.alter_column('app_metrics_gauge', 'name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Gauge.slug'
        db.alter_column('app_metrics_gauge', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=60, unique=True))
        # Adding unique constraint on 'Gauge', fields ['slug']
        db.create_unique('app_metrics_gauge', ['slug'])


    models = {
        'app_metrics.gauge': {
            'Meta': {'object_name': 'Gauge'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['company.Company']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'current_value': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'app_metrics.metric': {
            'Meta': {'unique_together': "(('slug', 'company'),)", 'object_name': 'Metric'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['company.Company']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '128'})
        },
        'app_metrics.metricday': {
            'Meta': {'object_name': 'MetricDay'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'app_metrics.metricitem': {
            'Meta': {'object_name': 'MetricItem'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'app_metrics.metricmonth': {
            'Meta': {'object_name': 'MetricMonth'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'app_metrics.metricset': {
            'Meta': {'object_name': 'MetricSet'},
            'email_recipients': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metrics': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['app_metrics.Metric']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'no_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send_daily': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'send_monthly': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'send_weekly': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'app_metrics.metricweek': {
            'Meta': {'object_name': 'MetricWeek'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'app_metrics.metricyear': {
            'Meta': {'object_name': 'MetricYear'},
            'created': ('django.db.models.fields.DateField', [], {'default': 'datetime.date.today'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['app_metrics.Metric']"}),
            'num': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'company.company': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('name', 'city', 'state', 'company_type'),)", 'object_name': 'Company'},
            'address_override': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'auto_add_direct_relationships': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geographic.City']", 'null': 'True'}),
            'company_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'confirmed_address': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'counties': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['geographic.County']", 'null': 'True', 'blank': 'True'}),
            'default_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'company_company_related'", 'null': 'True', 'to': "orm['auth.Group']"}),
            'home_page': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_customer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_eep_sponsor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'logo': ('stdimage.fields.StdImageField', [], {'blank': 'True', 'max_length': '100', 'upload_to': "'/documents/logos'", 'thumbnail_size': "{'width': 100, 'force': None, 'height': 100}", 'size': "{'width': 640, 'force': None, 'height': 480}"}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'office_phone': ('django.contrib.localflavor.us.models.PhoneNumberField', [], {'max_length': '20', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'sponsors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sponsored_companies'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['company.Company']"}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True'}),
            'street_line1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'street_line2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'geographic.city': {
            'Meta': {'ordering': "['county__state', 'county', 'name']", 'unique_together': "(('legal_statistical_area_description', 'county'),)", 'object_name': 'City'},
            'ansi_code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'county': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geographic.County']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_area_meters': ('django.db.models.fields.BigIntegerField', [], {}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'legal_statistical_area_description': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'place_fips': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'water_area_meters': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'geographic.climatezone': {
            'Meta': {'object_name': 'ClimateZone'},
            'doe_zone': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'moisture_regime': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'zone': ('django.db.models.fields.IntegerField', [], {})
        },
        'geographic.county': {
            'Meta': {'ordering': "['state', 'name']", 'unique_together': "(('legal_statistical_area_description', 'state'),)", 'object_name': 'County'},
            'ansi_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'climate_zone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geographic.ClimateZone']", 'null': 'True', 'blank': 'True'}),
            'county_fips': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'county_type': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'land_area_meters': ('django.db.models.fields.BigIntegerField', [], {}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'legal_statistical_area_description': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'metro': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['geographic.Metro']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2'}),
            'water_area_meters': ('django.db.models.fields.BigIntegerField', [], {})
        },
        'geographic.metro': {
            'Meta': {'object_name': 'Metro'},
            'cbsa_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }

    complete_apps = ['app_metrics']