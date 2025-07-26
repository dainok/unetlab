"""
Django settings for the UNetLab project.

This module contains the Django configuration for UNetLab,
including settings for Django core, REST framework, Celery, Channels, and Constance.
"""

import os
import socket
from pathlib import Path

# Base directory for the project
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# ⚠️ WARNING: In production, set the secret key in an environment variable!
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-is*$9*-@-)qo_%a^xo8i%ppjg2#qx4y)tl+ymhk+w*dfh64%pi",  # nosec
)

DEBUG = True  # Turn off in production

ALLOWED_HOSTS = []

# ==============================================================================
# APPLICATIONS
# ==============================================================================

INSTALLED_APPS = [
    # Core Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne",  # Must come before staticfiles for correct ASGI initialization
    "django.contrib.staticfiles",
    # Third-party apps
    "channels",  # WebSocket support
    "django_filters",  # Filters
    "django_tables2",  # Tables
    "rest_framework",  # API
    "rest_framework.authtoken",
    "constance",  # Dynamic settings backend
    # Local apps
    "ui",
    "job",
    "proxmox",
    # Optional: OpenAPI docs
    # "drf_spectacular",
    # "drf_spectacular_sidecar",
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Custom middlewares
    "unetlab.middleware.LoginRequiredMiddleware",
]

# ==============================================================================
# URL ROUTING
# ==============================================================================

ROOT_URLCONF = "unetlab.urls"

# ==============================================================================
# TEMPLATES CONFIGURATION
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Custom admin or UI templates
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

# ==============================================================================
# ASGI / WSGI APPLICATIONS
# ==============================================================================

WSGI_APPLICATION = "unetlab.wsgi.application"
ASGI_APPLICATION = "unetlab.asgi.application"

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ==============================================================================
# PASSWORD VALIDATORS
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ==============================================================================
# STATIC FILES
# ==============================================================================

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# CHANNEL LAYERS (WebSocket via Redis)
# ==============================================================================

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
            "prefix": "asgi",
        },
    },
}

# ==============================================================================
# DJANGO REST FRAMEWORK (DRF)
# ==============================================================================

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "DEFAULT_RENDERER_CLASSES": [
        "unetlab.renderers.CustomJSONRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "EXCEPTION_HANDLER": "unetlab.exception_handler.custom_exception_handler",
    "PAGE_SIZE": 10,
}

# ==============================================================================
# CELERY CONFIGURATION
# ==============================================================================

CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TASK_DEFAULT_QUEUE = "unetlab_default"

# Periodic tasks
CELERY_BEAT_SCHEDULE = {
    "cancel-stale-jobs": {
        "task": "job.tasks.job_cancel_stale_jobs",
        "schedule": 300.0,  # every 5 minutes
    },
}

# ==============================================================================
# LOGIN / LOGOUT REDIRECTS
# ==============================================================================

LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

# Public URLs excluded from login-required middleware
PUBLIC_URLS = [
    "login",
    "logout",
]

# ==============================================================================
# DJANGO-CONSTANCE (Dynamic settings)
# ==============================================================================

CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"

CONSTANCE_CONFIG = {
    "PROXMOX_PRIMARY_ADDRESS": (
        "",
        "The address of the primary Proxmox host.",
    ),
    "PROXMOX_USERNAME": (
        "root@pam",
        "The username used to log in to the Proxmox host.",
    ),
    "PROXMOX_TOKEN_ID": (
        "unetlab",
        "The Token ID associated with the Proxmox user.",
    ),
    "PROXMOX_SECRET": (
        "",
        "The secret used to authenticate to the Proxmox host.",
    ),
    "PROXMOX_VERIFY_SSL": (
        True,
        "Whether to verify the SSL certificate for Proxmox.",
    ),
    "PROXMOX_SHARED_STORAGE": (
        False,
        "Indicates if the Proxmox host uses shared storage for nodes and templates.",
    ),
}

# ==============================================================================
# HOST IDENTIFIER
# ==============================================================================

SOURCE = socket.gethostname().upper()

# ==============================================================================
# TABLES2 SETTINGS
# ==============================================================================

DJANGO_TABLES2_PAGE_SIZE = REST_FRAMEWORK["PAGE_SIZE"]
DJANGO_TABLES2_TEMPLATE = "unetlab/tables/table_full.html"
