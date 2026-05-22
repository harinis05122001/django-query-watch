# django_query_watch/analyzer.py

from collections import Counter
from .formatter import format_time, normalize_sql
from .settings import get_setting


def detect_slow_queries(queries: list) -> list:
    threshold = get_setting("SLOW_QUERY_THRESHOLD_MS")
    slow = []
    for q in queries:
        duration_ms = format_time(q.get("time", "0"))
        if duration_ms >= threshold:
            slow.append(
                {
                    "sql": q.get("sql", ""),
                    "duration_ms": duration_ms,
                }
            )
    return slow


def detect_duplicate_queries(queries: list) -> list:
    normalized = [normalize_sql(q.get("sql", "")) for q in queries]
    counts = Counter(normalized)
    duplicates = []
    seen = set()
    for q in queries:
        key = normalize_sql(q.get("sql", ""))
        if counts[key] > 1 and key not in seen:
            seen.add(key)
            duplicates.append(
                {
                    "sql": q.get("sql", ""),
                    "count": counts[key],
                }
            )
    return duplicates


def summarize_queries(queries: list, slow: list, duplicates: list) -> dict:
    total_time = sum(format_time(q.get("time", "0")) for q in queries)
    return {
        "total_queries": len(queries),
        "total_time_ms": round(total_time, 2),
        "slow_queries": len(slow),
        "duplicate_queries": len(duplicates),
    }
