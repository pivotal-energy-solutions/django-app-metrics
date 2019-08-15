# Django App Metrics

django-app-metrics allows you to capture and report on various events in your
applications.  You simply define various named metrics and record when they
happen.  These might be certain events that may be immediatey useful, for
example 'New User Signups', 'Downloads', etc.

Or they might not prove useful until some point in the future.  But if you
begin recording them now you'll have great data later on if you do need it.

For example 'Total Items Sold' isn't an exciting number when you're just
launching when you only care about revenue, but being able to do a contest
for the 1 millionth sold item in the future you'll be glad you were tracking
it.

You then group these individual metrics into a MetricSet, where you define
how often you want an email report being sent, and to which User(s) it should
be sent.

### Notes

## Documentation

Documentation can be found at [ReadTheDocs](http://django-app-metrics.readthedocs.org)

## Requirements

[Celery](http://celeryproject.org/) and [django-celery](http://ask.github.com/django-celery/)
must be installed, however if you do not wish to actually use Celery you can
simply set ``CELERY_ALWAYS_EAGER = True`` in your
settings and it will behave as if Celery was not configured.

## Usage


## Backends

``app_metrics.backends.db`` (Default) - This backend stores all metrics and
aggregations in your database. NOTE: Every call to ``metric()`` generates a
database write, which may decrease your overall performance is you go nuts
with them or have a heavily traffic site.

``app_metrics.backends.mixpanel`` - This backend allows you to pipe all of
your calls to ``metric()`` to Mixpanel. See the [Mixpanel documentation](http://mixpanel.com/docs/api-documentation)
for more information on their API.


``app_metrics.backends.statsd`` - This backend allows you to pipe all of your
calls to ``metric()`` to a statsd server. See [statsd](https://github.com/etsy/statsd) for more information
on their API.


``app_metrics.backends.redis`` - This backend allows you to use the metric() and
gauge() aspects, but not timer aspects of app_metrics.

``app_metrics.backends.librato_backend`` - This backend lets you send metrics to
Librato. See the [Librato documentation](http://dev.librato.com/v1/metrics#metrics) for more information on their API.
This requires the [Librato library]( http://pypi.python.org/pypi/librato/0.2). It uses use a librato Gauge by default,
although this can be overridden by supplying ``metric_type="counter"`` as a
keyword arg to ``metric()``.

``app_metrics.backends.composite`` - This backend lets you compose multiple
backends to which metric-calls are handed. The backends to which the call is
sent can be configured with the ``APP_METRICS_COMPOSITE_BACKENDS`` setting. This
can be overridden in each call by supplying a ``backends`` keyword argument::

    metric('signups', 42, backends=['app_metrics.backends.librato',
                                    'app_metrics.backends.db'])


## Settings

``APP_METRICS_BACKEND`` - Defaults to 'app_metrics.backends.db' if not defined.

``APP_METRICS_SEND_ZERO_ACTIVITY`` - Prevent e-mails being sent when there's been
no activity today (i.e. during testing). Defaults to `True`.

``APP_METRICS_DISABLED`` - If `True`, do not track metrics, useful for
debugging. Defaults to `False`.

### Mixpanel Settings

Set ``APP_METRICS_BACKEND`` == 'app_metrics.backends.mixpanel'.

``APP_METRICS_MIXPANEL_TOKEN`` - Your Mixpanel.com API token

``APP_METRICS_MIXPANEL_URL`` - Allow overriding of the API URL end point

### Statsd Settings

Set ``APP_METRICS_BACKEND`` == 'app_metrics.backends.statsd'.

``APP_METRICS_STATSD_HOST`` - Hostname of statsd server, defaults to 'localhost'

``APP_METRICS_STATSD_PORT`` - statsd port, defaults to '8125'

``APP_METRICS_STATSD_SAMPLE_RATE`` - statsd sample rate, defaults to 1

### Redis Settings

Set ``APP_METRICS_BACKEND`` == 'app_metrics.backends.redis'.

``APP_METRICS_REDIS_HOST`` - Hostname of redis server, defaults to 'localhost'

``APP_METRICS_REDIS_PORT`` - redis port, defaults to '6379'

``APP_METRICS_REDIS_DB`` - redis database number to use, defaults to 0

### Librato Settings

Set ``APP_METRICS_BACKEND`` == 'app_metrics.backends.librato'.

``APP_METRICS_LIBRATO_USER`` - Librato username

``APP_METRICS_LIBRATO_TOKEN`` - Librato API token

``APP_METRICS_LIBRATO_SOURCE`` - Librato data source (e.g. 'staging', 'dev'...)

### Composite Backend Settings

Set ``APP_METRICS_BACKEND`` == 'app_metrics.backends.composite'.

``APP_METRICS_COMPOSITE_BACKENDS`` - List of backends that are used by default,
e.g.::

    APP_METRICS_COMPOSITE_BACKENDS = ('librato', 'db', 'my_custom_backend',)

## Running the tests

To run the tests you'll need some requirements installed, so run::

    pip install -r requirements/test.txt

Then simply run::

    django-admin.py test --settings=app_metrics.tests.settings

## TODO

- Improve text and HTML templates to display trending data well


### Build Process:
1.  Update the `__version_info__` inside of the application. Commit and push.
2.  Tag the release with the version. `git tag <version> -m "Release"; git push --tags`
3.  Build the release `rm -rf dist build *egg-info; python setup.py sdist bdist_wheel`
4.  Upload the data `twine upload dist/*`