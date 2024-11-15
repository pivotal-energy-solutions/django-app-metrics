from django.core.management.base import BaseCommand

from app_metrics.models import MetricItem
from app_metrics.backends.mixpanel import metric
from app_metrics.utils import get_backend


class Command(BaseCommand):
    help = "Move MetricItems from the db backend to MixPanel"

    requires_model_validation = True

    def handle(self, **options):
        """Move MetricItems from the db backend to MixPanel" """

        backend = get_backend()

        # If not using Mixpanel this command is a NOOP
        if backend != "app_metrics.backends.mixpanel":
            print("You need to set the backend to MixPanel")
            return

        items = MetricItem.objects.all()

        for i in items:
            properties = {
                "time": i.created.strftime("%s"),
            }
            metric(i.metric.slug, num=i.num, properties=properties)

        # Kill off our items
        items.delete()
