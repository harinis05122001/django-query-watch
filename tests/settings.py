DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DJANGO_QUERY_WATCH = {
    "ENABLED": True,
    "SLOW_QUERY_THRESHOLD_MS": 0,
    "LOG_DUPLICATE_QUERIES": True,
    "LOG_QUERY_SUMMARY": True,
    "MAX_QUERY_PREVIEW_LENGTH": 500,
}
