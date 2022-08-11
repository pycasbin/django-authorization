import os
from pathlib import Path

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = "not-a-production-secret"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "casbin_adapter.apps.CasbinAdapterConfig",
    "dauthz.apps.DauthzConfig",
    "tests",
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

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

# CASBIN_MODEL = os.path.join(BASE_DIR, "tests", "dauthz-model.conf")

DAUTHZ = {
    'REQUEST_MIDDLEWARE': {
        'ENFORCER_NAME': 'DEFAULT',
    },
    'ENFORCER_MIDDLEWARE': {
        'ENFORCER_NAME': 'DEFAULT',
    },
    'ENFORCERS': {
        # Default Dauthz enforcer
        'DEFAULT': {
            # Casbin model setting.
            'MODEL': {
                # Available Settings: "file", "text"
                'CONFIG_TYPE': 'file',
                'CONFIG_FILE_PATH': Path(__file__).parent.joinpath('dauthz-model.conf'),
                'CONFIG_TEXT': '',
            },

            # Casbin adapter .
            'ADAPTER': 'casbin_adapter.adapter.Adapter',
            # Database setting.
            'STORAGE': {
                # Available Settings: "database", "file"
                'STORAGE_TYPE': 'database',
                # Database connection for following tables.
                'DATABASE_CONNECTION': '',
                # 'FILE_PATH':
            },

            'LOG': {
                # Changes whether Dauthz will log messages to the Logger.
                'ENABLED': False,
            },

            'CACHE': {

            },
        },
    }
}
