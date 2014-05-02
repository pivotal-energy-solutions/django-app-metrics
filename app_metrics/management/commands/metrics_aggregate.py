import datetime
import logging
from django.core.management.base import NoArgsCommand
from django.core.exceptions import MultipleObjectsReturned

from app_metrics.models import Metric, MetricItem, MetricDay, MetricWeek, MetricMonth, MetricYear

from app_metrics.utils import week_for_date, month_for_date, year_for_date, get_backend

log = logging.getLogger(__name__)

class Command(NoArgsCommand):
    help = "Aggregate Application Metrics"

    requires_model_validation = True

    def handle_noargs(self, **options):
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
                day,create = MetricDay.objects.get_or_create(metric=i.metric, created=i.created)
            except MultipleObjectsReturned:
                metrics = MetricDay.objects.filter(metric=i.metric)
                if metrics.count() > 1 and metrics.count() < 4:
                     metrics = metrics.exclude(id=metrics[0].id)
                     metrics.delete()
                else:
                    print("Multiple MetricDay found for Metric Item ({}) - {}".format(i.id, i))
                    raise

            day.num = day.num + i.num
            day.save()

            # Weekly Aggregation
            week_date = week_for_date(i.created)
            try:
                week, create = MetricWeek.objects.get_or_create(metric=i.metric, created=week_date)
            except MultipleObjectsReturned:
                metrics = MetricWeek.objects.filter(metric=i.metric)
                if metrics.count() > 1 and metrics.count() < 4:
                     metrics = metrics.exclude(id=metrics[0].id)
                     metrics.delete()
                else:
                    print("Multiple MetricWeek found for Metric Item ({}) - {}".format(i.id, i))
                    raise

            week.num = week.num + i.num
            week.save()

            # Monthly Aggregation
            month_date = month_for_date(i.created)
            try:
                month, create = MetricMonth.objects.get_or_create(metric=i.metric, created=month_date)
            except MultipleObjectsReturned:
                metrics = MetricMonth.objects.filter(metric=i.metric)
                if metrics.count() > 1 and metrics.count() < 4:
                     metrics = metrics.exclude(id=metrics[0].id)
                     metrics.delete()
                else:
                    print("Multiple MetricMonth found for Metric Item ({}) - {}".format(i.id, i))
                    raise

            month.num = month.num + i.num
            month.save()

            # Yearly Aggregation
            year_date = year_for_date(i.created)
            try:
                year, create = MetricYear.objects.get_or_create(metric=i.metric, created=year_date)
            except MultipleObjectsReturned:
                metrics = MetricYear.objects.filter(metric=i.metric)
                if metrics.count() > 1 and metrics.count() < 4:
                     metrics = metrics.exclude(id=metrics[0].id)
                     metrics.delete()
                else:
                    print("Multiple MetricYear found for Metric Item ({}) - {}".format(i.id, i))
                    raise

            year.num = year.num + i.num
            year.save()

        # Kill off our items
        items.delete()
