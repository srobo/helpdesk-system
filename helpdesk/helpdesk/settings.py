import platform
from pathlib import Path

import django_stubs_ext
import sentry_sdk
from django.core.exceptions import ImproperlyConfigured
from pkg_resources import parse_version

django_stubs_ext.monkeypatch()

#
# Environment setup
#

VERSION = "0.2.0-dev"

# Hostname
HOSTNAME = platform.node()

# Set the base directory two levels up
BASE_DIR = Path(__file__).resolve().parent.parent

# Validate Python version
if parse_version(platform.python_version()) < parse_version("3.9.0"):  # pragma: nocover
    raise RuntimeError(
        f"Helpdesk requires Python 3.9 or higher (current: Python {platform.python_version()})",
    )

#
# Configuration import
#

# Import configuration parameters
try:
    from helpdesk import configuration
except ImportError as e:  # pragma: nocover
    if getattr(e, "name") == "configuration":
        raise ImproperlyConfigured(
            "Configuration file is not present. Please define helpdesk/helpdesk/configuration.py per the documentation.",  # noqa: E501
        ) from None
    raise

sentry_sdk.init(
    dsn=getattr(configuration, "SENTRY_DSN", None),
    traces_sample_rate=getattr(configuration, "SENTRY_TRACES_SAMPLE_RATE", 1.0),
    profiles_sample_rate=getattr(configuration, "SENTRY_PROFILES_SAMPLE_RATE", 1.0),
)

# Enforce required configuration parameters
for parameter in ["ALLOWED_HOSTS", "DATABASE", "SECRET_KEY"]:
    if not hasattr(configuration, parameter):
        raise ImproperlyConfigured(  # pragma: nocover
            f"Required parameter {parameter} is missing from configuration.py.",
        )

# Set required parameters
ALLOWED_HOSTS = getattr(configuration, "ALLOWED_HOSTS")
DATABASE = getattr(configuration, "DATABASE")
SECRET_KEY = getattr(configuration, "SECRET_KEY")

# Set optional parameters
ADMINS = getattr(configuration, "ADMINS", [])
BASE_PATH = getattr(configuration, "BASE_PATH", "")
if BASE_PATH:
    BASE_PATH = BASE_PATH.strip("/") + "/"  # Enforce trailing slash only  # pragma: nocover
DEBUG = getattr(configuration, "DEBUG", False)
EMAIL = getattr(configuration, "EMAIL", {})
SYSTEM_TITLE = getattr(configuration, "SYSTEM_TITLE", "Helpdesk")
TIME_ZONE = getattr(configuration, "TIME_ZONE", "UTC")


#
# Database
#

DATABASES = {"default": DATABASE}


#
# Email
#

EMAIL_BACKEND = EMAIL.get("BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = EMAIL.get("SERVER")
EMAIL_HOST_USER = EMAIL.get("USERNAME")
EMAIL_HOST_PASSWORD = EMAIL.get("PASSWORD")
EMAIL_PORT = EMAIL.get("PORT", 25)
EMAIL_SSL_CERTFILE = EMAIL.get("SSL_CERTFILE")
EMAIL_SSL_KEYFILE = EMAIL.get("SSL_KEYFILE")
EMAIL_SUBJECT_PREFIX = EMAIL.get("SUBJECT_PREFIX", "[Helpdesk] ")
EMAIL_USE_SSL = EMAIL.get("USE_SSL", False)
EMAIL_USE_TLS = EMAIL.get("USE_TLS", False)
EMAIL_TIMEOUT = EMAIL.get("TIMEOUT", 10)
SERVER_EMAIL = EMAIL.get("FROM_EMAIL")


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

SRCOMP_HTTP_BASE_URL = getattr(configuration, "SRCOMP_HTTP_BASE_URL", None)
VOLUNTEER_SIGNUP_CODE = getattr(configuration, "VOLUNTEER_SIGNUP_CODE")


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
