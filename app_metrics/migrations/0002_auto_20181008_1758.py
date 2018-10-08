# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-08 17:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_metrics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='metricset',
            name='email_recipients',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='email recipients'),
        ),
        migrations.AddField(
            model_name='metricset',
            name='metrics',
            field=models.ManyToManyField(to='app_metrics.Metric', verbose_name='metrics'),
        ),
        migrations.AddField(
            model_name='metricmonth',
            name='metric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_metrics.Metric', verbose_name=b'metric'),
        ),
        migrations.AddField(
            model_name='metricitem',
            name='metric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_metrics.Metric', verbose_name='metric'),
        ),
        migrations.AddField(
            model_name='metricday',
            name='metric',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_metrics.Metric', verbose_name='metric'),
        ),
        migrations.AddField(
            model_name='metric',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.Company'),
        ),
        migrations.AddField(
            model_name='gauge',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='company.Company'),
        ),
        migrations.AlterUniqueTogether(
            name='metric',
            unique_together=set([('slug', 'company')]),
        ),
    ]
