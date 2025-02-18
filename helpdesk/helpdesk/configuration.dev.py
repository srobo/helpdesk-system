##############################################################
#  This file serves as a base configuration for development  #
#  only. It is not intended for production use.              #
##############################################################

ALLOWED_HOSTS = ["localhost"]

SECRET_KEY = "django-insecure-rT1%IHNOY&jAn9b-7(uoOdlVKb(giEcBhMK$6+sGp3UO-X^FPe"  # noqa: S105

DEBUG = True

EMAIL = {
    "BACKEND": "django.core.mail.backends.console.EmailBackend",
}

VOLUNTEER_SIGNUP_CODE = "testing"
