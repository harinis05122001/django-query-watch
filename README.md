# django-query-watch

> Lightweight Django query performance monitoring and debugging toolkit.

[![PyPI version](https://badge.fury.io/py/django-query-watch.svg)](https://pypi.org/project/django-query-watch/)
[![Python](https://img.shields.io/pypi/pyversions/django-query-watch)](https://pypi.org/project/django-query-watch/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/harinis05122001/django-query-watch/actions/workflows/ci.yml/badge.svg)](https://github.com/harinis05122001/django-query-watch/actions)

---

## What is this?

`django-query-watch` is a developer tool that monitors your Django application's database queries in real time — directly in your terminal.

It helps you catch:

- **Slow queries** exceeding a configurable threshold
- **Duplicate queries** caused by N+1 problems
- **Per-request summaries** showing total query count and execution time

No dashboards. No admin panels. Just clean, readable terminal output while you develop.

---

## Features

- Slow query detection with configurable threshold
- Duplicate / N+1 query detection
- Per-request query summary
- Rich colored terminal output
- Zero frontend dependencies
- Minimal overhead
- Works with PostgreSQL, MySQL, and SQLite

---

## Installation

```bash
pip install django-query-watch
```

---

## Quick Start

**1. Add to `INSTALLED_APPS`:**

```python
INSTALLED_APPS = [
    ...
    "django_query_watch",
]
```

**2. Add middleware:**

```python
MIDDLEWARE = [
    ...
    "django_query_watch.middleware.QueryWatchMiddleware",
]
```

**3. Run your server:**

```bash
python manage.py runserver
```

That's it. Query monitoring starts automatically.

---

## Configuration

Add this to your `settings.py` to customize behavior:

```python
DJANGO_QUERY_WATCH = {
    "ENABLED": True,
    "SLOW_QUERY_THRESHOLD_MS": 200,
    "LOG_DUPLICATE_QUERIES": True,
    "LOG_QUERY_SUMMARY": True,
    "MAX_QUERY_PREVIEW_LENGTH": 500,
}
```

| Setting                    | Default | Description                          |
| -------------------------- | ------- | ------------------------------------ |
| `ENABLED`                  | `True`  | Enable or disable the package        |
| `SLOW_QUERY_THRESHOLD_MS`  | `200`   | Threshold in ms to flag slow queries |
| `LOG_DUPLICATE_QUERIES`    | `True`  | Detect and log duplicate queries     |
| `LOG_QUERY_SUMMARY`        | `True`  | Print per-request summary            |
| `MAX_QUERY_PREVIEW_LENGTH` | `500`   | Max SQL characters shown in logs     |

---

## Example Output

**Slow query detected:**

```
╭─ [DJANGO-QUERY-WATCH] ⚠ Slow Query Detected ────────────────╮
│                                                               │
│  Execution Time: 423ms                                        │
│  Request:        /api/orders/                                 │
│                                                               │
│  SQL:                                                         │
│  SELECT * FROM shop_product WHERE ...                         │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
```

**Duplicate query detected (N+1):**

```
╭─ [DJANGO-QUERY-WATCH] ⚠ Duplicate Query Detected ───────────╮
│                                                               │
│  Repeated: 18 times                                           │
│                                                               │
│  SQL:                                                         │
│  SELECT * FROM shop_category WHERE id = 1                     │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
```

**Request summary:**

```
╭─ [DJANGO-QUERY-WATCH] ✔ Request Summary ────────────────────╮
│                                                               │
│  Path:              /api/products/                            │
│  Total Queries:     1                                         │
│  Total Time:        1.0ms                                     │
│  Slow Queries:      0                                         │
│  Duplicate Queries: 0                                         │
│                                                               │
╰───────────────────────────────────────────────────────────────╯
```

---

## Common Use Cases

**Catching N+1 queries:**

```python
# Bad — triggers N+1
for product in Product.objects.all():
    print(product.category.name)  # query per product

# Good — single query
for product in Product.objects.select_related("category").all():
    print(product.category.name)
```

`django-query-watch` will flag the first version with duplicate query warnings and show you exactly which SQL is repeating.

---

## Why this exists

Django's ORM makes it easy to write queries that look clean but perform badly at scale. Tools like Django Debug Toolbar are great but require a browser and add significant setup. `django-query-watch` gives you instant terminal feedback with zero friction — just add the middleware and start developing.

---

## Requirements

- Python 3.10+
- Django 4.0+
- Works with DEBUG = True (development only)

---

## Roadmap

- [ ] Query export to JSON/CSV
- [ ] OpenTelemetry integration
- [ ] Async support
- [ ] Prometheus metrics
- [ ] Optional admin dashboard

---

## Contributing

Pull requests are welcome. For major changes please open an issue first.

```bash
git clone https://github.com/harinis05122001/django-query-watch
cd django-query-watch
python -m venv venv
source venv/bin/activate
pip install -e .
pytest tests/ -v
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
