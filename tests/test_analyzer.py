import pytest
from django_query_watch.analyzer import (
    detect_slow_queries,
    detect_duplicate_queries,
    summarize_queries,
)

SAMPLE_QUERIES = [
    {"sql": "SELECT * FROM shop_product", "time": "0.050"},
    {"sql": "SELECT * FROM shop_category WHERE id = 1", "time": "0.300"},
    {"sql": "SELECT * FROM shop_category WHERE id = 1", "time": "0.300"},
    {"sql": "SELECT * FROM shop_category WHERE id = 1", "time": "0.300"},
]


def test_detect_slow_queries():
    slow = detect_slow_queries(SAMPLE_QUERIES)
    assert len(slow) > 0
    assert all("duration_ms" in q for q in slow)
    assert all("sql" in q for q in slow)


def test_slow_query_threshold():
    queries = [{"sql": "SELECT 1", "time": "0.001"}]
    slow = detect_slow_queries(queries)
    assert len(slow) == 1


def test_detect_duplicate_queries():
    duplicates = detect_duplicate_queries(SAMPLE_QUERIES)
    assert len(duplicates) == 1
    assert duplicates[0]["count"] == 3


def test_no_duplicates_when_all_unique():
    queries = [
        {"sql": "SELECT * FROM a", "time": "0.001"},
        {"sql": "SELECT * FROM b", "time": "0.001"},
    ]
    duplicates = detect_duplicate_queries(queries)
    assert len(duplicates) == 0


def test_summarize_queries():
    slow = detect_slow_queries(SAMPLE_QUERIES)
    dupes = detect_duplicate_queries(SAMPLE_QUERIES)
    summary = summarize_queries(SAMPLE_QUERIES, slow, dupes)

    assert summary["total_queries"] == 4
    assert summary["total_time_ms"] > 0
    assert "slow_queries" in summary
    assert "duplicate_queries" in summary


def test_empty_queries():
    slow = detect_slow_queries([])
    dupes = detect_duplicate_queries([])
    summary = summarize_queries([], slow, dupes)

    assert summary["total_queries"] == 0
    assert summary["total_time_ms"] == 0.0
