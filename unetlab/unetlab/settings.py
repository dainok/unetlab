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
    'DJANGO_SECRET_KEY',
    'django-insecure-is*$9*-@-)qo_%a^xo8i%ppjg2#qx4y)tl+ymhk+w*dfh64%pi',  #
)

DEBUG = True  # Turn off in production

ALLOWED_HOSTS = ['*']

# ==============================================================================
# APPLICATIONS
# ==============================================================================

INSTALLED_APPS = [
    # Core Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'daphne',  # Must come before staticfiles for correct ASGI initialization
    'django.contrib.staticfiles',
    # Third-party apps
    'channels',  # WebSocket support
    'django_filters',  # Filters
    'django_tables2',  # Tables
    'rest_framework',  # API
    'rest_framework.authtoken',
    'constance',  # Dynamic settings backend
    # Local apps
    'ui',
    # "job",
    'lab',
    'node',
    # "proxmox",
    # "repository",
    # Optional: OpenAPI docs
    # "drf_spectacular",
    # "drf_spectacular_sidecar",
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # I18N
]

# ==============================================================================
# URL ROUTING
# ==============================================================================

ROOT_URLCONF = 'unetlab.urls'

# ==============================================================================
# TEMPLATES CONFIGURATION
# ==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Custom admin or UI templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==============================================================================
# ASGI / WSGI APPLICATIONS
# ==============================================================================

WSGI_APPLICATION = 'unetlab.wsgi.application'
ASGI_APPLICATION = 'unetlab.asgi.application'

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ==============================================================================
# PASSWORD VALIDATORS
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

# Add django.middleware.locale.LocaleMiddleware to MIDDLEWARE
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = [
    BASE_DIR / 'i18n',
]

# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# CHANNEL LAYERS (WebSocket via Redis)
# ==============================================================================

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('localhost', 6379)],
            'prefix': 'asgi',
        },
    },
}

# ==============================================================================
# CELERY CONFIGURATION
# ==============================================================================

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TASK_DEFAULT_QUEUE = 'unetlab_default'

# Periodic tasks
CELERY_BEAT_SCHEDULE = {
    'cancel-stale-jobs': {
        'task': 'job.tasks.job_cancel_stale_jobs',
        'schedule': 300.0,  # every 5 minutes
    },
}

# ==============================================================================
# HOST IDENTIFIER
# ==============================================================================

SOURCE = socket.gethostname().upper()

# ==============================================================================
# FILE UPLOAD
# ==============================================================================

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440
DATA_UPLOAD_MAX_MEMORY_SIZE = 104857600
MEDIA_ROOT = BASE_DIR / '..' / 'uploads'
MEDIA_URL = '/files/'

# ==============================================================================
# UI: LOGIN / LOGOUT REDIRECTS
# ==============================================================================

LOGIN_REDIRECT_URL = 'home'  # "/accounts/login/"
LOGOUT_REDIRECT_URL = 'login'  # "/accounts/logout/"

# ==============================================================================
# UI: STATIC FILES
# ==============================================================================

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# ==============================================================================
# UI: DJANGO CONSTANCE (Dynamic settings)
# ==============================================================================

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'PROXMOX_PRIMARY_ADDRESS': (
        '',
        'The address of the primary Proxmox host.',
    ),
    'PROXMOX_VERIFY_SSL': (
        True,
        'Whether to verify the SSL certificate for Proxmox.',
    ),
    'PROXMOX_USERNAME': (
        'root@pam',
        'The username used to log in to the Proxmox host.',
    ),
    'PROXMOX_SECRET': (
        '',
        'The secret used to authenticate to the Proxmox host.',
    ),
    'PROXMOX_TOKEN_ID': (
        'unetlab',
        'The Token ID associated with the Proxmox user.',
    ),
    'TEMPLATE_DIR': (
        f'{BASE_DIR.parent}/templates/local.json',
        'Directory where to store Proxmox templates.',
    ),
}

# ==============================================================================
# UI: DJANGO REST FRAMEWORK (DRF)
# ==============================================================================

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'ui.include.pagination.CustomPagination',
    'DEFAULT_RENDERER_CLASSES': ['ui.renderers.CustomJSONRenderer'],
    'EXCEPTION_HANDLER': 'ui.exception_handler.CustomExceptionHandler',
    'MAX_PAGE_SIZE': 100,
    'PAGE_SIZE': 10,
}

# ==============================================================================
# UI: DJANGO TABLES2 SETTINGS
# ==============================================================================

DJANGO_TABLES2_MAX_PAGE_SIZE = REST_FRAMEWORK['MAX_PAGE_SIZE']
DJANGO_TABLES2_PAGE_SIZE = REST_FRAMEWORK['PAGE_SIZE']
DJANGO_TABLES2_TEMPLATE = 'ui/tables/table_full.html'

# ==============================================================================
# UI: HTML COMPONENTS
# ==============================================================================

SITE_META = {
    'title': 'Unified Networking Lab',
    'authors': [
        'Andrea Dainese',
    ],
    'description': 'UNetLab is a modular and extensible orchestration platform tailored for virtual network '
    + 'environments. It provides centralized control over distributed compute resources, enabling automated '
    + 'provisioning, scheduling, and lifecycle management of virtual nodes and jobs. Designed for testing and '
    + 'production, UNetLab ensures a scalable and secure foundation for building reproducible network labs and '
    + 'automation pipelines.',
    'keywords': [
        'virtualization',
        'orchestration',
        'network',
        'automation',
        'unetlab',
    ],
}

SITE_NAVBAR = [
    {
        'text': 'Home',
        'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        + 'class="icon icon-1"><path d="M5 12l-2 0l9 -9l9 9l-2 0"></path>'
        + '<path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7"></path>'
        + '<path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6"></path></svg>',
        'view': 'home',
    },
    {
        'text': 'System',
        'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        + 'class="icon icon-1"><path d="M12 3l8 4.5l0 9l-8 4.5l-8 -4.5l0 -9l8 -4.5"></path>'
        + '<path d="M12 12l8 -4.5"></path><path d="M12 12l0 9"></path><path d="M12 12l-8 -4.5"></path>'
        + '<path d="M16 5.25l-8 4.5"></path></svg>',
        'dropdown': [
            {
                'text': 'Groups',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-tabler icons-tabler-outline icon-tabler-users"><path stroke="none" d="M0 0h24v24H0z" '
                + 'fill="none" /><path d="M9 7m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0" />'
                + '<path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /><path d="M16 3.13a4 4 0 0 1 0 7.75" />'
                + '<path d="M21 21v-2a4 4 0 0 0 -3 -3.85" /></svg>',
                'view': 'group_list',
            },
            # {
            #     "text": "Hosts",
            #     "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" ' + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' + 'class="icon icon-tabler icons-tabler-outline icon-tabler-server"><path stroke="none" d="M0 0h24v24H0z" ' + 'fill="none" /><path d="M3 4m0 3a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v2a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3z" /><path d="M3 12m0 3a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v2a3 3 0 0 1 -3 3h-12a3 3 0 0 1 -3 -3z" /><path d="M7 8l0 .01" /><path d="M7 16l0 .01" /></svg>',
            #     "view": "host_list",
            # },
            # {
            #     "text": "Jobs",
            #     "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" ' + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' + 'class="icon icon-tabler icons-tabler-outline icon-tabler-stack-2"><path stroke="none" d="M0 0h24v24H0z" ' + 'fill="none" /><path d="M12 4l-8 4l8 4l8 -4l-8 -4" /><path d="M4 12l8 4l8 -4" /><path d="M4 16l8 4l8 -4" /></svg>',
            #     "view": "job_list",
            # },
            # {
            #     "text": "Logs",
            #     "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" ' + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' + 'class="icon icon-tabler icons-tabler-outline icon-tabler-align-box-left-top"><path stroke="none" d="M0 0h24v24H0z" ' + 'fill="none" /><path d="M3 3m0 2a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2z" /><path d="M9 13h-2" /><path d="M13 10h-6" /><path d="M11 7h-4" /></svg>',
            #     "view": "log_list",
            # },
            {
                'text': 'Settings',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-1"><path d="M10.325 4.317c.426 -1.756 2.924 -1.756 3.35 0a1.724 1.724 0 0 0 2.573 '
                + '1.066c1.543 -.94 3.31 .826 2.37 2.37a1.724 1.724 0 0 0 1.065 2.572c1.756 .426 1.756 2.924 0 '
                + '3.35a1.724 1.724 0 0 0 -1.066 2.573c.94 1.543 -.826 3.31 -2.37 2.37a1.724 1.724 0 0 0 -2.572 '
                + '1.065c-.426 1.756 -2.924 1.756 -3.35 0a1.724 1.724 0 0 0 -2.573 -1.066c-1.543 .94 -3.31 -.826 '
                + '-2.37 -2.37a1.724 1.724 0 0 0 -1.065 -2.572c-1.756 -.426 -1.756 -2.924 0 -3.35a1.724 1.724 0 0 0 '
                + '1.066 -2.573c-.94 -1.543 .826 -3.31 2.37 -2.37c1 .608 2.296 .07 2.572 -1.065z"></path>'
                + '<path d="M9 12a3 3 0 1 0 6 0a3 3 0 0 0 -6 0"></path></svg>',
                'view': 'settings_list',
            },
            {
                'text': 'Templates',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-tabler icons-tabler-outline icon-tabler-template"><path stroke="none" d="M0 0h24v24H0z" '
                + 'fill="none"></path><path d="M4 4m0 1a1 1 0 0 1 1 -1h14a1 1 0 0 1 1 1v2a1 1 0 0 1 -1 1h-14a1 1 0 0 '
                + '1 -1 -1z"></path><path d="M4 12m0 1a1 1 0 0 1 1 -1h4a1 1 0 0 1 1 1v6a1 1 0 0 1 -1 1h-4a1 1 0 0 1 '
                + '-1 -1z"></path><path d="M14 12l6 0"></path><path d="M14 16l6 0"></path>'
                + '<path d="M14 20l6 0"></path></svg>',
                'view': 'nodetemplate_list',
            },
            {
                'text': 'Tokens',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-tabler icons-tabler-outline icon-tabler-key"><path stroke="none" d="M0 0h24v24H0z" '
                + 'fill="none" /><path d="M16.555 3.843l3.602 3.602a2.877 2.877 0 0 1 0 4.069l-2.643 2.643a2.877 2.877 0 0 1 -4.069 0l-.301 -.301l-6.558 6.558a2 2 0 0 1 -1.239 .578l-.175 .008h-1.172a1 1 0 0 1 -.993 -.883l-.007 -.117v-1.172a2 2 0 0 1 .467 -1.284l.119 -.13l.414 -.414h2v-2h2v-2l2.144 -2.144l-.301 -.301a2.877 2.877 0 0 1 0 -4.069l2.643 -2.643a2.877 2.877 0 0 1 4.069 0z" /><path d="M15 9h.01" /></svg>',
                'view': 'token_list',
            },
            {
                'text': 'Users',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-tabler icons-tabler-outline icon-tabler-user"><path stroke="none" d="M0 0h24v24H0z" '
                + 'fill="none" /><path d="M8 7a4 4 0 1 0 8 0a4 4 0 0 0 -8 0" /><path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2" /></svg>',
                'view': 'user_list',
            },
        ],
    },
    {
        'text': 'Workspace',
        'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        + 'class="icon icon-1"><path d="M4 4m0 2a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v1a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z"></path><path d="M4 13m0 2a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v3a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z"></path><path d="M14 4m0 2a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v3a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z"></path><path d="M14 15m0 2a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v1a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z"></path></svg>',
        'dropdown': [
            {
                'text': 'Labs',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-tabler icons-tabler-outline icon-tabler-clipboard"><path stroke="none" d="M0 0h24v24H0z" '
                + 'fill="none" /><path d="M9 5h-2a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-12a2 2 0 0 0 -2 -2h-2" /><path d="M9 3m0 2a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v0a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z" /></svg>',
                'view': 'lab_list',
            },
            #         {
            #             "text": "Running labs",
            #             "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" ' + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' + 'class="icon icon-tabler icons-tabler-outline icon-tabler-clipboard-data"><path stroke="none" d="M0 0h24v24H0z" ' + 'fill="none" /><path d="M9 5h-2a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-12a2 2 0 0 0 -2 -2h-2" /><path d="M9 3m0 2a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v0a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z" /><path d="M9 17v-4" /><path d="M12 17v-1" /><path d="M15 17v-2" /><path d="M12 17v-1" /></svg>',
            #             "view": "labinstance_list",
            #         },
            #         {
            #             "text": "Nodes",
            #             "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" ' + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' + 'class="icon icon-tabler icons-tabler-outline icon-tabler-layers-intersect"><path stroke="none" d="M0 0h24v24H0z" ' + 'fill="none"></path><path d="M8 4m0 2a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v8a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2z"></path><path d="M4 8m0 2a2 2 0 0 1 2 -2h8a2 2 0 0 1 2 2v8a2 2 0 0 1 -2 2h-8a2 2 0 0 1 -2 -2z"></path></svg>',
            #             "url": "#tbd",
            #         },
            #         {
            #             "text": "Gateways",
            #             "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" ' + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' + 'class="icon icon-tabler icons-tabler-outline icon-tabler-cloud-network"><path stroke="none" d="M0 0h24v24H0z" ' + 'fill="none"></path><path d="M3 20h7"></path><path d="M14 20h7"></path><path d="M10 20a2 2 0 1 0 4 0a2 2 0 0 0 -4 0"></path><path d="M12 16v2"></path><path d="M8 16.004h-1.343c-2.572 -.004 -4.657 -2.011 -4.657 -4.487c0 -2.475 2.085 -4.482 4.657 -4.482c.393 -1.762 1.794 -3.2 3.675 -3.773c1.88 -.572 3.956 -.193 5.444 1c1.488 1.19 2.162 3.007 1.77 4.769h.99c1.913 0 3.464 1.56 3.464 3.486c0 1.927 -1.551 3.487 -3.465 3.487h-2.535"></path></svg>',
            #             "url": "#tbd",
            #         },
            #         {
            #             "text": "Links",
            #             "svg": '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" ' + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" ' + 'class="icon icon-tabler icons-tabler-outline icon-tabler-timeline-event"><path stroke="none" d="M0 0h24v24H0z" ' + 'fill="none"></path><path d="M12 20m-2 0a2 2 0 1 0 4 0a2 2 0 1 0 -4 0"></path><path d="M10 20h-6"></path><path d="M14 20h6"></path><path d="M12 15l-2 -2h-3a1 1 0 0 1 -1 -1v-8a1 1 0 0 1 1 -1h10a1 1 0 0 1 1 1v8a1 1 0 0 1 -1 1h-3l-2 2z"></path></svg>',
            #             "url": "#tbd",
            #         },
        ],
    },
    {
        'text': 'Help',
        'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
        + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
        + 'class="icon icon-1"><path d="M12 12m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0"></path><path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"></path><path d="M15 15l3.35 3.35"></path><path d="M9 15l-3.35 3.35"></path><path d="M5.65 5.65l3.35 3.35"></path><path d="M18.35 5.65l-3.35 3.35"></path></svg></span>',
        'dropdown': [
            {
                'text': 'Changelog',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-tabler icons-tabler-outline icon-tabler-align-box-left-top"><path stroke="none" d="M0 0h24v24H0z" '
                + 'fill="none"></path><path d="M3 3m0 2a2 2 0 0 1 2 -2h14a2 2 0 0 1 2 2v14a2 2 0 0 1 -2 2h-14a2 2 0 0 1 -2 -2z"></path><path d="M9 13h-2"></path><path d="M13 10h-6"></path><path d="M11 7h-4"></path></svg>',
                'url': '#tbd',
            },
            {
                'text': 'Contribute',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-tabler icons-tabler-outline icon-tabler-contract"><path stroke="none" d="M0 0h24v24H0z" '
                + 'fill="none" /><path d="M8 21h-2a3 3 0 0 1 -3 -3v-1h5.5" /><path d="M17 8.5v-3.5a2 2 0 1 1 2 2h-2" /><path d="M19 3h-11a3 3 0 0 0 -3 3v11" /><path d="M9 7h4" /><path d="M9 11h4" /><path d="M18.42 12.61a2.1 2.1 0 0 1 2.97 2.97l-6.39 6.42h-3v-3z" /></svg>',
                'url': '#tbd',
            },
            {
                'text': 'Documentation',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-1"><path d="M5 12l-2 0l9 -9l9 9l-2 0"></path><path d="M5 12v7a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-7"></path><path d="M9 21v-6a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v6"></path></svg>',
                'url': '#tbd',
            },
            {
                'text': 'Feedback',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-tabler icons-tabler-outline icon-tabler-message"><path stroke="none" d="M0 0h24v24H0z" '
                + 'fill="none" /><path d="M8 9h8" /><path d="M8 13h6" /><path d="M18 4a3 3 0 0 1 3 3v8a3 3 0 0 1 -3 3h-5l-5 3v-3h-2a3 3 0 0 1 -3 -3v-8a3 3 0 0 1 3 -3h12z" /></svg>',
                'url': '#tbd',
            },
            {
                'text': 'Source code',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-2"><path d="M9 19c-4.3 1.4 -4.3 -2.5 -6 -3m12 5v-3.5c0 -1 .1 -1.4 -.5 -2c2.8 -.3 5.5 -1.4 5.5 -6a4.6 4.6 0 0 0 -1.3 -3.2a4.2 4.2 0 0 0 -.1 -3.2s-1.1 -.3 -3.5 1.3a12.3 12.3 0 0 0 -6.2 0c-2.4 -1.6 -3.5 -1.3 -3.5 -1.3a4.2 4.2 0 0 0 -.1 3.2a4.6 4.6 0 0 0 -1.3 3.2c0 4.6 2.7 5.7 5.5 6c-.6 .6 -.6 1.2 -.5 2v3.5"></path></svg>',
                'url': 'https://github.com/dainok/unetlab/',
            },
            {
                'text': 'Sponsor',
                'css': 'text-pink',
                'svg': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" '
                + 'fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
                + 'class="icon icon-inline me-1 icon-2"><path d="M19.5 12.572l-7.5 7.428l-7.5 -7.428a5 5 0 1 1 7.5 -6.566a5 5 0 1 1 7.5 6.572"></path></svg>',
                'url': 'https://www.patreon.com/c/adainese/membership',
            },
        ],
    },
]
