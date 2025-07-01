"""Django settings for UNetLab project."""

__author__ = "Andrea Dainese"
__contact__ = "andrea@adainese.it"
__copyright__ = "Copyright 2024, Andrea Dainese"
__license__ = "GPLv3"

import os
import socket
from datetime import datetime

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-is*$9*-@-)qo_%a^xo8i%ppjg2#qx4y)tl+ymhk+w*dfh64%pi"  # nosec
)

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne",
    "django.contrib.staticfiles",
    "constance",
    "channels",
    # "rest_framework",
    "job",  # UNetLab: job and log management
    "proxmox",  # UNetLab: Proxmox host management
    # "drf_spectacular",
    # "drf_spectacular_sidecar",
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

ROOT_URLCONF = "unetlab.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],  # Add custom admin template
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

WSGI_APPLICATION = "unetlab.wsgi.application"

ASGI_APPLICATION = "unetlab.asgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Post login and logout redirects

LOGIN_REDIRECT_URL = "home"

LOGOUT_REDIRECT_URL = "home"

# Channel configuration for WebSockets
# https://channels.readthedocs.io/en/stable/topics/channel_layers.html

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
            # "hosts":[{
            #     "address": "rediss://user@host:port",  # "REDIS_TLS_URL"
            #     "ssl_cert_reqs": None,
            # }],
            "prefix": "asgi",
        },
    },
}

# Celery configuration
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_DEFAULT_QUEUE = "unetlab_default"
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_BEAT_SCHEDULE = {
    "cancel-stale-jobs": {
        "task": "job.tasks.job_cancel_stale_jobs",
        "schedule": 300.0,  # every 5 minutes
    },
}

# Constance backend
# https://django-constance.readthedocs.io/en/latest/backends.html#backends

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_CONFIG = {
    "PROXMOX_PRIMARY_ADDRESS": (
        "",
        "The address of the primary Proxmox host.",
    ),
    "PROXMOX_USERNAME": (
        "root@pam",
        "The username used for logging into the Proxmox host.",
    ),
    "PROXMOX_TOKEN_ID": (
        "unetlab",
        "The Token ID associated to the Proxmox username.",
    ),
    "PROXMOX_SECRET": (
        "",
        "The secret used for logging into the Proxmox host.",
    ),
    "PROXMOX_VERIFY_SSL": (
        True,
        "True if the backend is required to verify the SSL certificates of the Proxmox host.",
    ),
    "PROXMOX_SHARED_STORAGE": (
        False,
        "True if the Proxmox host has shared storage for storing nodes and templates.",
    ),
    "PROXMOX_UPDATED_AT": (
        datetime.now(),
        "The last time the Proxmox hosts were checked.",
    ),
}

SOURCE = socket.gethostname().upper()
