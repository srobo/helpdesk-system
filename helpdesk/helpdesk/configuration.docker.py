import os

import dj_database_url

ALLOWED_HOSTS = ["*"]

DATABASE = dj_database_url.config(
    conn_max_age=600,
    conn_health_checks=True,
)

SECRET_KEY = os.environ.get("SECRET_KEY", "insecure")

DEBUG = False

EMAIL = {
    "BACKEND": "django.core.mail.backends.dummy.EmailBackend",
}

TIME_ZONE = "Europe/London"

SYSTEM_TITLE = "SR2023 Helpdesk"
VOLUNTEER_SIGNUP_CODE = os.environ.get("VOLUNTEER_SIGNUP_CODE")
SRCOMP_HTTP_BASE_URL = "https://srcomp.studentrobotics.org/comp-api"
