from unittest import skipIf

from django.test import TestCase
from django.core.exceptions import ImproperlyConfigured


from app_metrics.utils import *  # noqa: F403

skip_tests = settings.APP_METRICS_MIXPANEL_TOKEN is None


class MixpanelMetricConfigTests(TestCase):
    def setUp(self):
        self.old_backend = settings.APP_METRICS_BACKEND
        settings.APP_METRICS_BACKEND = "app_metrics.backends.mixpanel"

    def test_metric(self):
        self.assertRaises(ImproperlyConfigured, metric, "test_metric")

    def tearDown(self):
        settings.APP_METRICS_BACKEND = self.old_backend


class MixpanelCreationTests(TestCase):
    def setUp(self):
        self.old_backend = settings.APP_METRICS_BACKEND
        self.old_token = settings.APP_METRICS_MIXPANEL_TOKEN
        settings.APP_METRICS_BACKEND = "app_metrics.backends.mixpanel"
        settings.APP_METRICS_MIXPANEL_TOKEN = "foobar"

    @skipIf(skip_tests, "Missing Mixpanel token")
    def test_metric(self):
        metric("testing")

    def tearDown(self):
        settings.APP_METRICS_BACKEND = self.old_backend
        settings.APP_METRICS_MIXPANEL_TOKEN = self.old_token
