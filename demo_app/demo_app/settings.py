"""
Django settings for demo_app project.

Generated by 'django-admin startproject' using Django 2.2.17.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import logging
import os
import sys

import environ

env = environ.Env(
    DEBUG=(bool, False),
    DEBUG_LEVEL=(int, logging.WARNING),
    SECRET_KEY=(str, "SECRET_KEY"),
    MARIADB_DATABASE=(str, "db"),
    MARIADB_USER=(str, "root"),
    MARIADB_PASSWORD=(str, "password"),
    MARIADB_HOST=(str, "127.0.0.1"),
    MARIADB_PORT=(str, "3306"),
    RABBITMQ_DEFAULT_USER=(str, "guest"),
    RABBITMQ_DEFAULT_PASS=(str, "password"),
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env.read_env(env_file=os.path.join(os.path.dirname(BASE_DIR), ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "company.apps.CompanyConfig",
    "eep_program.apps.EEPProgramConfig",
    "relationship.apps.RelationshipConfig",
    "app_metrics",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "demo_app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "demo_app.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("MARIADB_DATABASE"),
        "USER": env("MARIADB_USER"),
        "PASSWORD": env("MARIADB_PASSWORD"),
        "HOST": env("MARIADB_HOST"),
        "PORT": env("DOCKER_MYSQL_PORT", default=env("MARIADB_PORT", default="3306")),
        "OPTIONS": {"charset": "utf8mb4"},
        "TEST": {
            "MIGRATE": False,
            "CHARSET": "utf8mb4",
            "COLLATION": "utf8mb4_unicode_520_ci",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] - %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "django": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "django.request": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.security": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.server": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.db.backends": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.template": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "celery": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "amqp": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "kombu": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "requests": {"handlers": ["console"], "level": "WARNING"},
        "multiprocessing": {"handlers": ["console"], "level": "WARNING"},
        "py.warnings": {"handlers": ["console"], "level": "WARNING"},
        "demo_app": {
            "handlers": ["console"],
            "level": env("DEBUG_LEVEL", "ERROR"),
            "propagate": False,
        },
        "": {"handlers": ["console"], "level": env("DEBUG_LEVEL", "ERROR"), "propagate": True},
    },
}

CELERY_BROKER_USER = env("RABBITMQ_DEFAULT_USER", default="guest")
CELERY_BROKER_PASSWORD = env("RABBITMQ_DEFAULT_PASS", default="password")
CELERY_BROKER_HOST = env("RABBITMQ_HOST", default="127.0.0.1")
CELERY_BROKER_VHOST = env("RABBITMQ_DEFAULT_VHOST", default="/")
CELERY_BROKER_PORT = env("DOCKER_RABBITMQ_PORT", default="5563")

CELERY_BROKER_URL = "amqp://{0}:{1}@{2}:{3}{4}".format(
    CELERY_BROKER_USER,
    CELERY_BROKER_PASSWORD,
    CELERY_BROKER_HOST,
    CELERY_BROKER_PORT,
    CELERY_BROKER_VHOST,
)

CELERY_TASK_ALWAYS_EAGER = True
CELERY_ALWAYS_EAGER = True

APP_METRICS_BACKEND = "app_metrics.backends.db"
APP_METRICS_MIXPANEL_TOKEN = None
APP_METRICS_DISABLED = False
