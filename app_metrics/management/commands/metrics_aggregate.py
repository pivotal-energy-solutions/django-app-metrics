import datetime
import logging
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

from app_metrics.models import Metric, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricYear

from app_metrics.utils import week_for_date, month_for_date, year_for_date, get_backend

log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Aggregate Application Metrics"

    requires_model_validation = True

    def handle(self, **options):
        """ Aggregate Application Metrics """

        backend = get_backend()

        # If using Mixpanel this command is a NOOP
        if backend == 'app_metrics.backends.mixpanel':
            print "Useless use of metrics_aggregate when using Mixpanel backend"
            return

        # Aggregate Items
        items = MetricItem.objects.all()

        for i in items:
            # Daily Aggregation
            try:
                days = MetricDay.objects.filter(metric=i.metric, created=i.created)
            except ObjectDoesNotExist:
                day,create = MetricDay.objects.get_or_create(metric=i.metric, created=i.created)
            else:
                if days.count() > 1:
                     days = days.exclude(id=days[0].id)
                     days.delete()
                try:
                    day = days[0]
                except IndexError:
                    day,create = MetricDay.objects.get_or_create(metric=i.metric, created=i.created)

            day.num = day.num + i.num
            day.save()

            # Weekly Aggregation
            week_date = week_for_date(i.created)
            try:
                weeks = MetricWeek.objects.filter(metric=i.metric, created=week_date)
            except ObjectDoesNotExist:
                week,create = MetricWeek.objects.get_or_create(metric=i.metric, created=week_date)
            else:
                if weeks.count() > 1:
                     weeks = weeks.exclude(id=weeks[0].id)
                     weeks.delete()
                try:
                    week = weeks[0]
                except IndexError:
                    week,create = MetricWeek.objects.get_or_create(metric=i.metric, created=week_date)

            week.num = week.num + i.num
            week.save()

            # Monthly Aggregation
            month_date = month_for_date(i.created)
            try:
                months = MetricMonth.objects.filter(metric=i.metric, created=month_date)
            except ObjectDoesNotExist:
                month,create = MetricMonth.objects.get_or_create(metric=i.metric, created=month_date)
            else:
                if months.count() > 1:
                     months = months.exclude(id=months[0].id)
                     months.delete()
                try:
                    month = months[0]
                except IndexError:
                    month,create = MetricMonth.objects.get_or_create(metric=i.metric, created=month_date)

            # Yearly Aggregation
            year_date = year_for_date(i.created)
            try:
                years = MetricYear.objects.filter(metric=i.metric, created=year_date)
            except ObjectDoesNotExist:
                years,create = MetricYear.objects.get_or_create(metric=i.metric, created=year_date)
            else:
                if years.count() > 1:
                     years = years.exclude(id=years[0].id)
                     years.delete()
                try:
                    year = years[0]
                except IndexError:
                    year,create = MetricYear.objects.get_or_create(metric=i.metric, created=year_date)

            year.num = year.num + i.num
            year.save()

        # Kill off our items
        items.delete()
