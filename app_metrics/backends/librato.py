# -*- coding: utf-8 -*-
from app_metrics.tasks import librato_metric_task


def _get_func(_async):
    return librato_metric_task.delay if _async else librato_metric_task


def metric(slug, num=1, _async=True, **kwargs):
    _get_func(_async)(slug, num, metric_type="counter", **kwargs)


def timing(slug, seconds_taken, _async=True, **kwargs):
    """not implemented"""


def gauge(slug, current_value, _async=True, **kwargs):
    _get_func(_async)(slug, current_value, metric_type="gauge", **kwargs)
