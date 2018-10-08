# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-08 17:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gauge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('slug', models.SlugField(max_length=128, verbose_name='slug')),
                ('current_value', models.DecimalField(decimal_places=6, default=b'0.00', max_digits=15, verbose_name='current value')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='updated')),
            ],
            options={
                'verbose_name': 'gauge',
                'verbose_name_plural': 'gauges',
            },
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('slug', models.SlugField(max_length=128, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'metric',
                'verbose_name_plural': 'metrics',
            },
        ),
        migrations.CreateModel(
            name='MetricDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.BigIntegerField(default=0, verbose_name='number')),
                ('created', models.DateField(default=datetime.date.today, verbose_name='created')),
            ],
            options={
                'ordering': ('created', 'metric'),
                'verbose_name': 'day metric',
                'verbose_name_plural': 'day metrics',
            },
        ),
        migrations.CreateModel(
            name='MetricItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.IntegerField(default=1, verbose_name='number')),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='created')),
            ],
            options={
                'verbose_name': 'metric item',
                'verbose_name_plural': 'metric items',
            },
        ),
        migrations.CreateModel(
            name='MetricMonth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.BigIntegerField(default=0, verbose_name='number')),
                ('created', models.DateField(default=datetime.date.today, verbose_name='created')),
            ],
            options={
                'ordering': ('created', 'metric'),
                'verbose_name': 'month metric',
                'verbose_name_plural': 'month metrics',
            },
        ),
        migrations.CreateModel(
            name='MetricSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('no_email', models.BooleanField(default=False, verbose_name='no e-mail')),
                ('send_daily', models.BooleanField(default=True, verbose_name='send daily')),
                ('send_weekly', models.BooleanField(default=False, verbose_name='send weekly')),
                ('send_monthly', models.BooleanField(default=False, verbose_name='send monthly')),
            ],
            options={
                'verbose_name': 'metric set',
                'verbose_name_plural': 'metric sets',
            },
        ),
        migrations.CreateModel(
            name='MetricWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.BigIntegerField(default=0, verbose_name='number')),
                ('created', models.DateField(default=datetime.date.today, verbose_name='created')),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_metrics.Metric', verbose_name='metric')),
            ],
            options={
                'ordering': ('created', 'metric'),
                'verbose_name': 'week metric',
                'verbose_name_plural': 'week metrics',
            },
        ),
        migrations.CreateModel(
            name='MetricYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num', models.BigIntegerField(default=0, verbose_name='number')),
                ('created', models.DateField(default=datetime.date.today, verbose_name='created')),
                ('metric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_metrics.Metric', verbose_name='metric')),
            ],
            options={
                'ordering': ('created', 'metric'),
                'verbose_name': 'year metric',
                'verbose_name_plural': 'year metrics',
            },
        ),
    ]
