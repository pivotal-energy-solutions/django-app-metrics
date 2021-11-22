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


DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
}

SILENCED_SYSTEM_CHECKS = ["django_mysql.E016"]
