# -*- coding: utf-8 -*-
"""celery.py - simulation"""

import os
import logging

from celery import Celery

log = logging.getLogger(__name__)

__author__ = "Steven K"
__date__ = "5/28/20 12:14"
__copyright__ = "Copyright 2011-2020 Pivotal Energy Solutions. All rights reserved."
__credits__ = [
    "Steven K",
]


# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_app.settings")

app = Celery("proj")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
