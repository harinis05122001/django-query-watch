# django_query_watch/middleware.py

from django.db import connection, reset_queries
from django.conf import settings

from .settings import is_enabled, get_setting
from .analyzer import detect_slow_queries, detect_duplicate_queries, summarize_queries
from .logger import log_slow_query, log_duplicate_query, log_summary


class QueryWatchMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not is_enabled() or not settings.DEBUG:
            return self.get_response(request)

        reset_queries()

        response = self.get_response(request)

        queries = connection.queries

        if not queries:
            return response

        slow = detect_slow_queries(queries)
        duplicates = detect_duplicate_queries(queries)
        summary = summarize_queries(queries, slow, duplicates)

        for q in slow:
            log_slow_query(
                sql=q["sql"],
                duration_ms=q["duration_ms"],
                request_path=request.path,
            )

        if get_setting("LOG_DUPLICATE_QUERIES"):
            for d in duplicates:
                log_duplicate_query(sql=d["sql"], count=d["count"])

        if get_setting("LOG_QUERY_SUMMARY"):
            log_summary(path=request.path, summary=summary)

        return response
