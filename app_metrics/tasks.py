import base64
import json
import datetime
import logging
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import dateutil.parser
from django.utils.timezone import now as utcnow

from celery import shared_task

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import IntegrityError

from app_metrics.models import Metric, MetricItem, Gauge

# For statsd support
try:
    # Not required. If we do this once at the top of the module, we save
    # ourselves the pain of importing every time the task fires.
    import statsd
except ImportError:
    statsd = None

# For redis support
try:
    import redis
except ImportError:
    redis = None

# For librato support
try:
    import librato
    from librato.metrics import Gauge as LibratoGauge
    from librato.metrics import Counter as LibratoCounter
except ImportError:
    librato = None

log = logging.getLogger("celery.task")


class MixPanelTrackError(Exception):
    pass


@shared_task
def db_metric_task(num=1, **kwargs):
    """This is a task to add a metric item"""
    if getattr(settings, "DEBUG"):
        log.setLevel(logging.DEBUG)
    created = kwargs.pop("created", utcnow())
    if isinstance(created, str):
        try:
            created = dateutil.parser.parse(created).replace(tzinfo=datetime.timezone.utc)
        except Exception as err:
            log.error("Unable to parse date from {} - {}".format(created, err))
            created = utcnow()
    try:
        met, _ = Metric.objects.get_or_create(**kwargs)
        MetricItem.objects.create(metric=met, num=num, created=created)
    except IntegrityError:
        met, _ = Metric.objects.get(**kwargs)
        MetricItem.objects.create(metric=met, num=num, created=created)
    except Exception as err:
        issue = "Unable to complete task!! {} - kwargs: {}".format(err, kwargs)
        log.exception(issue)
        raise


@shared_task
def db_gauge_task(current_value, **kwargs):
    """This is a task to adjust (or create) a guage"""
    if getattr(settings, "DEBUG"):
        log.setLevel(logging.DEBUG)

    if "defaults" not in kwargs.keys():
        kwargs["defaults"] = {}
    kwargs["defaults"]["current_value"] = current_value
    gauge, created = Gauge.objects.get_or_create(**kwargs)
    if not created:
        gauge.current_value = current_value
        gauge.save()
    log.debug("{} Gauge {} to {}".format("Created" if created else "Updated", gauge, current_value))


def _get_token():
    token = getattr(settings, "APP_METRICS_MIXPANEL_TOKEN", None)

    if not token:
        raise ImproperlyConfigured(
            "You must define APP_METRICS_MIXPANEL_TOKEN when using the mixpanel backend."
        )
    else:
        return token


# Mixpanel tasks


@shared_task
def mixpanel_metric_task(slug, num, properties=None, **kwargs):
    token = _get_token()
    if properties is None:
        properties = dict()

    if "token" not in properties:
        properties["token"] = token

    url = getattr(settings, "APP_METRICS_MIXPANEL_API_URL", "http://api.mixpanel.com/track/")

    params = {"event": slug, "properties": properties}
    b64_data = base64.b64encode(json.dumps(params).encode())

    data = urlencode({"data": b64_data}).encode()
    req = Request(url, data)
    for i in range(num):
        response = urlopen(req)
        if response.read() == "0":
            raise MixPanelTrackError("MixPanel returned 0")


# Statsd tasks


def get_statsd_conn():
    if statsd is None:
        raise ImproperlyConfigured("You must install 'python-statsd' in order to use this backend.")

    conn = statsd.Connection(
        host=getattr(settings, "APP_METRICS_STATSD_HOST", "localhost"),
        port=int(getattr(settings, "APP_METRICS_STATSD_PORT", 8125)),
        sample_rate=float(getattr(settings, "APP_METRICS_STATSD_SAMPLE_RATE", 1)),
    )
    return conn


@shared_task
def statsd_metric_task(slug, num=1, **kwargs):
    conn = get_statsd_conn()
    counter = statsd.Counter(slug, connection=conn)
    counter += num


@shared_task
def statsd_timing_task(slug, seconds_taken=1.0, **kwargs):
    conn = get_statsd_conn()

    # You might be wondering "Why not use ``timer.start/.stop`` here?"
    # The problem is that this is a task, likely running out of process
    # & perhaps with network overhead. We'll measure the timing elsewhere,
    # in-process, to be as accurate as possible, then use the out-of-process
    # task for talking to the statsd backend.
    timer = statsd.Timer(slug, connection=conn)
    timer.send("total", seconds_taken)


@shared_task
def statsd_gauge_task(slug, current_value, **kwargs):
    conn = get_statsd_conn()
    gauge = statsd.Gauge(slug, connection=conn)
    # We send nothing here, since we only have one name/slug to work with here.
    gauge.send("", current_value)


# Redis tasks


def get_redis_conn():
    if redis is None:
        raise ImproperlyConfigured("You must install 'redis' in order to use this backend.")
    conn = redis.StrictRedis(
        host=getattr(settings, "APP_METRICS_REDIS_HOST", "localhost"),
        port=getattr(settings, "APP_METRICS_REDIS_PORT", 6379),
        db=getattr(settings, "APP_METRICS_REDIS_DB", 0),
    )
    return conn


@shared_task
def redis_metric_task(slug, num=1, **kwargs):
    # Record a metric in redis. We prefix our key here with 'm' for Metric
    # and build keys for each day, week, month, and year
    r = get_redis_conn()

    # Build keys
    now = datetime.datetime.now()
    day_key = "m:%s:%s" % (slug, now.strftime("%Y-%m-%d"))
    week_key = "m:%s:w:%s" % (slug, now.strftime("%U"))
    month_key = "m:%s:m:%s" % (slug, now.strftime("%Y-%m"))
    year_key = "m:%s:y:%s" % (slug, now.strftime("%Y"))

    # Increment keys
    r.incrby(day_key, num)
    r.incrby(week_key, num)
    r.incrby(month_key, num)
    r.incrby(year_key, num)


@shared_task
def redis_gauge_task(slug, current_value, **kwargs):
    # We prefix our keys with a 'g' here for Gauge to avoid issues
    # of having a gauge and metric of the same name
    r = get_redis_conn()
    r.set("g:%s" % slug, current_value)


# Librato tasks


@shared_task
def librato_metric_task(name, num, attributes=None, metric_type="gauge", **kwargs):
    connection = librato.connect(
        settings.APP_METRICS_LIBRATO_USER, settings.APP_METRICS_LIBRATO_TOKEN
    )

    if metric_type == "counter":
        metric = LibratoCounter(connection, name, attributes=attributes)
    else:
        metric = LibratoGauge(connection, name, attributes=attributes)

    metric.add(num, source=settings.APP_METRICS_LIBRATO_SOURCE)
