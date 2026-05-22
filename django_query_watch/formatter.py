# django_query_watch/formatter.py

import re
from .settings import get_setting


def truncate_sql(sql: str) -> str:
    max_length = get_setting("MAX_QUERY_PREVIEW_LENGTH")
    sql = sql.strip()
    if len(sql) > max_length:
        return sql[:max_length] + "  ... [truncated]"
    return sql


def format_time(seconds: str) -> float:
    """Convert Django's query time string (seconds) to milliseconds."""
    try:
        return round(float(seconds) * 1000, 2)
    except (ValueError, TypeError):
        return 0.0


def normalize_sql(sql: str) -> str:
    """Strip extra whitespace for duplicate comparison."""
    return re.sub(r"\s+", " ", sql.strip().lower())
