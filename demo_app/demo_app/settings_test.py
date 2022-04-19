# -*- coding: utf-8 -*-
from __future__ import absolute_import

import warnings

from .settings import *


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None


MIGRATION_MODULES = DisableMigrations()

# Handle system warning as log messages
warnings.simplefilter("once")


mysql_db = DATABASES["default"]
DEFAULT_DB = {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
if os.environ.get("DB_TYPE") == "mysql":
    print("Using MySQL Backend!")
    DEFAULT_DB = mysql_db

DATABASES = {
    "default": DEFAULT_DB,
}

CELERY_TASK_ALWAYS_EAGER = CELERY_TASK_EAGER_PROPAGATES = True
CELERYD_HIJACK_ROOT_LOGGER = True

DJANGO_TEST_PROCESSES = 4

SILENCED_SYSTEM_CHECKS = ["django_mysql.E016"]
