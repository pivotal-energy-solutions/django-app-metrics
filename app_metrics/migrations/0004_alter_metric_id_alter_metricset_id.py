# -*- coding: utf-8 -*-
# Generated by Django 4.0.7 on 2022-09-15 18:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app_metrics", "0003_alter_gauge_current_value_alter_gauge_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="metric",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="metricset",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
