import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"
if DEBUG:
    SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY") or get_random_secret_key()
else:
    SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,[::1]").split(",")
    if host.strip()
]

ROOT_URLCONF = "triumf_site.urls"
WSGI_APPLICATION = "triumf_site.wsgi.application"

INSTALLED_APPS = ["django.contrib.staticfiles", "team"]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
    }
]

LANGUAGE_CODE = "ru"
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
