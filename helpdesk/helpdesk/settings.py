import platform
from pathlib import Path

import django_stubs_ext
import sentry_sdk
from environ import Env

django_stubs_ext.monkeypatch()

Env.read_env()

env = Env(
    DEBUG=(bool, True),
    SENTRY_DSN=(str, ""),
    ALLOWED_HOSTS=(list, ["*"]),
    SECRET_KEY=(str, "django-insecure-rT1%IHNOY&jAn9b-7(uoOdlVKb(giEcBhMK$6+sGp3UO-X^FPe"),
    BASE_PATH=(str, ""),
    SRCOMP_HTTP_BASE_URL=(str, ""),
    VOLUNTEER_SIGNUP_CODE=(str, "sr")
)

#
# Environment setup
#

# Hostname
HOSTNAME = platform.node()

# Set the base directory two levels up
BASE_DIR = Path(__file__).resolve().parent.parent

sentry_sdk.init(
    dsn=env("SENTRY_DSN"),
    traces_sample_rate=0,
    profiles_sample_rate=0,
)

ALLOWED_HOSTS = env("ALLOWED_HOSTS")

SECRET_KEY = env("SECRET_KEY")

BASE_PATH = env("BASE_PATH")
if BASE_PATH:
    BASE_PATH = BASE_PATH.strip("/") + "/"  # Enforce trailing slash only  # pragma: nocover


DEBUG = env("DEBUG")
SYSTEM_TITLE = "Helpdesk"
TIME_ZONE = "Europe/London"


#
# Database
#

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite",
    }
}

#
# Django
#

INSTALLED_APPS = [
    "accounts",
    "display",
    "helpdesk",
    "teams",
    "tickets",
    "crispy_forms",
    "crispy_bulma",
    "django_filters",
    "django_tables2",
    "django_tables2_bulma_template",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "accounts.middleware.ProfileMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "helpdesk.urls"

SITE_ID = 1

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "helpdesk.context_processors.settings_context",
            ],
        },
    },
]

WSGI_APPLICATION = "helpdesk.wsgi.application"

AUTH_USER_MODEL = "accounts.User"

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

LANGUAGE_CODE = "en-gb"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = str(BASE_DIR) + "/static"
STATIC_URL = f"/{BASE_PATH}static/"

# Authentication URLs
LOGIN_URL = f"/{BASE_PATH}auth/login/"
LOGOUT_REDIRECT_URL = LOGIN_URL
LOGIN_REDIRECT_URL = f"/{BASE_PATH}"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Crispy
CRISPY_ALLOWED_TEMPLATE_PACKS = ("bulma",)
CRISPY_TEMPLATE_PACK = "bulma"

# Django Tables 2
DJANGO_TABLES2_TEMPLATE = "django-tables2/bulma.html"

# Django AllAuth

ACCOUNT_ADAPTER = "helpdesk.account_adapter.AccountAdapter"
ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    },
}

# Application

SRCOMP_HTTP_BASE_URL = env("SRCOMP_HTTP_BASE_URL")
VOLUNTEER_SIGNUP_CODE = env("VOLUNTEER_SIGNUP_CODE")


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # Send logs with at least INFO level to the console.
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s][%(process)d][%(levelname)s][%(name)s] %(message)s",
        },
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
