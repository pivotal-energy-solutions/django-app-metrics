# -*- coding: utf-8 -*-
class AppMetricsError(Exception):
    pass


class InvalidMetricsBackend(AppMetricsError):
    pass


class MetricError(AppMetricsError):
    pass


class TimerError(AppMetricsError):
    pass
