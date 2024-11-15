# Generated by Django 4.0.7 on 2022-09-15 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app_metrics", "0002_auto_20181008_1758"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gauge",
            name="current_value",
            field=models.DecimalField(
                decimal_places=6, default="0.00", max_digits=15, verbose_name="current value"
            ),
        ),
        migrations.AlterField(
            model_name="gauge",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="metricday",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="metricitem",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="metricmonth",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="metricmonth",
            name="metric",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="app_metrics.metric",
                verbose_name="metric",
            ),
        ),
        migrations.AlterField(
            model_name="metricweek",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="metricyear",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
