# examples/demo_project/config/settings.py

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-demo-key-not-for-production"

DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
    "shop",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django_query_watch.middleware.QueryWatchMiddleware",
]

ROOT_URLCONF = "config.urls"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# django-query-watch config
DJANGO_QUERY_WATCH = {
    "ENABLED": True,
    "SLOW_QUERY_THRESHOLD_MS": 1,  # set low so demo triggers warnings easily
    "LOG_DUPLICATE_QUERIES": True,
    "LOG_QUERY_SUMMARY": True,
    "MAX_QUERY_PREVIEW_LENGTH": 500,
}
