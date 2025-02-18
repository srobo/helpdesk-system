from __future__ import annotations

#########################
#                       #
#   Required settings   #
#                       #
#########################

# This is a list of valid fully-qualified domain names (FQDNs) for the Helpdesk server. Helpdesk will not permit write
# access to the server via any other hostnames. The first FQDN in the list will be treated as the preferred name.
#
# Example: ALLOWED_HOSTS = ['helpdesk.example.com', 'helpdesk.internal.local']

ALLOWED_HOSTS: list[str] = []

# This key is used for secure generation of random numbers and strings. It must never be exposed outside of this file.
# For optimal security, SECRET_KEY should be at least 50 characters in length and contain a mix of letters, numbers, and
# symbols. Helpdesk will not run without this defined. For more information, see
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-SECRET_KEY
SECRET_KEY = ""

#########################
#                       #
#   Optional settings   #
#                       #
#########################

# Specify one or more name and email address tuples representing Helpdesk administrators. These people will be notified
# of application errors (assuming correct email settings are provided).
ADMINS: list[tuple[str, str]] = [
    # ('John Doe', 'jdoe@example.com'),
]

# Base URL path if accessing Helpdesk within a directory. For example, if installed at https://example.com/helpdesk/,
# set BASE_PATH = 'helpdesk/'
BASE_PATH = ""

# Set to True to enable server debugging. WARNING: Debugging introduces a substantial performance penalty and may reveal
# sensitive information about your installation. Only enable debugging while performing testing. Never enable debugging
# on a production system.
DEBUG = False

EMAIL: dict[str, str | int | bool] = {
    # 'SERVER': '',
    # 'USERNAME': '',
    # 'PASSWORD': '',
    # 'PORT': 25,
    # 'SSL_CERTFILE': '',
    # 'SSL_KEYFILE': '',
    # 'SUBJECT_PREFIX': '[Helpdesk] ',
    # 'USE_SSL': False,
    # 'USE_TLS': False,
    # 'TIMEOUT': 10,
    # 'FROM_EMAIL': 'helpdesk@example.com',
}

# Title of the System
SYSTEM_TITLE = "Helpdesk"

# Time zone (default: UTC)
TIME_ZONE = "UTC"

VOLUNTEER_SIGNUP_CODE = "testing"
