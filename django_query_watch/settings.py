# django_query_watch/settings.py

from django.conf import settings
from .constants import DEFAULT_SETTINGS


def get_setting(key: str):
    user_settings = getattr(settings, "DJANGO_QUERY_WATCH", {})
    return user_settings.get(key, DEFAULT_SETTINGS[key])


def is_enabled() -> bool:
    return get_setting("ENABLED")
